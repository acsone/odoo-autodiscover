#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

from __future__ import print_function

import os
from os.path import join as opj
import re
import shutil
import subprocess
import tempfile
from textwrap import dedent

import pytest


class OdooVirtualenv:

    def __init__(self, series, editable, python, preset_venv, cache):
        self.series = series
        self.editable = editable
        self.python = python
        self.preset_venv = preset_venv
        self.cache = cache
        self.odoo_base_dir = str(cache.makedir('odoo'))
        self.venv_dir = None
        self.tmp_dir = None

    def setUp(self):
        if self.preset_venv:
            self.venv_dir = self.preset_venv
        else:
            self.tmp_dir = tempfile.mkdtemp()
            self.venv_dir = opj(self.tmp_dir, 'venv')
            make_venv_cmd = [self.python, '-m', 'virtualenv', self.venv_dir]
            subprocess.check_call(make_venv_cmd)
            self.pip_install('-U', 'setuptools')
            self.pip_install_odoo()
            self.pip_install_odoo_autodiscover()

    def tearDown(self):
        if self.tmp_dir:
            shutil.rmtree(self.tmp_dir)

    def raise_unsupported(self):
        raise RuntimeError("Unsupported Odoo series %s" % self.series)

    @property
    def python_bin(self):
        return opj(self.venv_dir, 'bin', 'python')

    @property
    def odoo_bin(self):
        if self.series in ('8.0', '9.0'):
            return opj(self.venv_dir, 'bin', 'openerp-server')
        elif self.series in ('10.0', '11.0'):
            return opj(self.venv_dir, 'bin', 'odoo')
        else:
            self.raise_unsupported()

    @property
    def root_dir(self):
        return os.path.abspath(opj(os.path.dirname(__file__), '..'))

    @property
    def odoo_dir(self):
        return opj(self.odoo_base_dir, self.series)

    def pip_install(self, *args):
        cmd = [opj(self.venv_dir, 'bin', 'pip'), 'install'] + list(args)
        subprocess.check_call(cmd)

    def pip_uninstall(self, name):
        cmd = [opj(self.venv_dir, 'bin', 'pip'), 'uninstall', '-y', name]
        subprocess.check_call(cmd)
        # TODO remove trailing *-nspkg.pth file to work around pip issue
        #      https://github.com/pypa/pip/issues/4176

    def pip_install_odoo_autodiscover(self):
        self.pip_install(self.root_dir)

    def pip_install_odoo_dependencies(self):
        requirements = opj(self.odoo_dir, 'requirements.txt')
        args = [
            '-f', 'https://wheelhouse.acsone.eu/manylinux1',
            '-r', requirements,
        ]
        self.pip_install(*args)

    def download_odoo(self):
        if os.path.exists(self.odoo_dir):
            return
        url = 'https://github.com/odoo/odoo.git'
        if self.series in ('8.0', '9.0', '10.0'):
            branch = self.series
        elif self.series == '11.0':
            branch = 'master'
        else:
            self.raise_unsupported()
        cmd = ['git', 'clone', '--depth=1', '-b', branch, url, self.odoo_dir]
        subprocess.check_call(cmd)

    def pip_install_odoo(self):
        self.download_odoo()
        self.pip_install_odoo_dependencies()
        if self.editable:
            self.pip_install('-e', self.odoo_dir)
        else:
            self.pip_install(self.odoo_dir)

    def check_import_odoo(self):
        if self.series in ('8.0', '9.0'):
            subprocess.check_call(
                [self.python_bin, '-c', 'from openerp import api'])
        elif self.series in ('10.0', '11.0'):
            subprocess.check_call(
                [self.python_bin, '-c', 'from odoo import api'])
        else:
            self.raise_unsupported()
        #
        # all versions
        #
        # this is a use case from openupgradelib
        script = dedent("""
        try:
            from odoo.exceptions import UserError
        except ImportError:
            from openerp.exceptions import Warning as UserError
        """)
        subprocess.check_call([self.python_bin, '-c', script])

    def pip_install_test_addon(self, name, editable):
        addon_dir = opj(self.root_dir, 'tests', 'addons', self.series, name)
        if editable:
            self.pip_install('-e', addon_dir)
        else:
            self.pip_install(addon_dir)

    def get_addons_paths(self):
        cmd = [self.odoo_bin, '--stop-after-init']
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        addons_path_re = re.compile(r'addons paths: (\[.*?\])', re.MULTILINE)
        mo = addons_path_re.search(output)
        if not mo:
            raise RuntimeError('Addons path not found in\n{}'.format(output))
        return eval(mo.group(1))

    def _has_site_packages(self, addons_paths):
        for ap in addons_paths:
            if 'site-packages' in ap:
                return True
        return False

    def _has_odoo_dir(self, addons_paths):
        assert self.editable
        # resolve symlinks because odoo addons paths have symlink resolved
        real_odoo_dir = os.path.realpath(self.odoo_dir)
        for ap in addons_paths:
            if real_odoo_dir in ap:
                return True
        return False

    def _has_addon_dir(self, addons_paths, addon_name):
        if self.series in ('8.0', '9.0'):
            nspkg = 'odoo_addons'
        elif self.series in ('10.0', '11.0'):
            nspkg = opj('odoo', 'addons')
        else:
            self.raise_unsupported()
        match = opj(addon_name, nspkg)
        for ap in addons_paths:
            if match in ap:
                return True
        return False

    def check_addons_paths(self, editable_addons=[], not_editable_addons=[]):
        addons_paths = self.get_addons_paths()
        if self.editable:
            assert self._has_odoo_dir(addons_paths)
        if not not_editable_addons and self.editable:
            assert not self._has_site_packages(addons_paths)
        if not_editable_addons or not self.editable:
            assert self._has_site_packages(addons_paths)
        for addon_name in editable_addons:
            assert self._has_addon_dir(addons_paths, addon_name)


ODOO_VENV_PARAMS = [
    ('11.0', False, 'python3', None),
    ('11.0', True, 'python3', None),
    ('11.0', False, 'python2', None),
    ('11.0', True, 'python2', None),
    ('10.0', False, 'python2', None),
    ('10.0', True, 'python2', None),
    ('9.0', False, 'python2', None),
    ('9.0', True, 'python2', None),
    ('8.0', False, 'python2', None),
    ('8.0', True, 'python2', None),
]


def _add_param_from_environ():
    preset_venv = os.environ.get('ODOO_AUTODISCOVER_PRESET_VENV')
    if not preset_venv:
        return
    # find installed Odoo version by parsing `pip list` output
    pip_list = subprocess.check_output(
        [opj(preset_venv, 'bin', 'pip'), 'list', '--format=legacy'],
        universal_newlines=True)
    odoo_re = r'^odoo \(([0-9][0-9]?\.0)[^ ]*(\)|.+\))$'
    mo = re.search(odoo_re, pip_list, re.MULTILINE)
    if not mo:
        raise RuntimeError("Odoo not installed in {}?".format(preset_venv))
    series = mo.group(1)
    editable = (mo.group(2) != ')')
    ODOO_VENV_PARAMS.append((series, editable, None, preset_venv))


_add_param_from_environ()


def _make_odoo_venv_ids():
    venv_ids = []
    for series, editable, python, preset_venv in ODOO_VENV_PARAMS:
        if preset_venv:
            venv_ids.append('{series}-preset'.format(**locals()))
        else:
            if editable:
                editable = '-editable'
            else:
                editable = ''
            venv_ids.append('{series}{editable}-{python}'.format(**locals()))
    return venv_ids


ODOO_VENV_IDS = _make_odoo_venv_ids()


@pytest.fixture(scope="function", params=ODOO_VENV_PARAMS, ids=ODOO_VENV_IDS)
def odoo_venv(request):
    series, editable, python, preset_venv = request.param
    venv = OdooVirtualenv(
        series, editable, python, preset_venv, request.config.cache)
    try:
        venv.setUp()
        yield venv
    finally:
        venv.tearDown()
