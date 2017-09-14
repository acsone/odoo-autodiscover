#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

from __future__ import print_function

import contextlib
import os
from os.path import join as opj
import re
import shutil
import subprocess
import tempfile

import requests
import pytest


@contextlib.contextmanager
def DirectoryChanger(d):
    cwd = os.getcwd()
    os.chdir(d)
    try:
        yield
    finally:
        os.chdir(cwd)


class OdooVirtualenv:

    def __init__(self, series, editable, preset_venv, cache):
        self.series = series
        self.editable = editable
        self.preset_venv = preset_venv
        self.cache = cache
        self.odoo_base_dir = str(cache.makedir('odoo'))
        self.venv_dir = None
        self.tmpd = None

    def setUp(self):
        if self.preset_venv:
            self.venv_dir = self.preset_venv
        else:
            self.check_virtualenv_installed()
            self.tmpd = tempfile.mkdtemp()
            self.venv_dir = opj(self.tmpd, 'venv')
            if self.series in ('8.0', '9.0', '10.0'):
                make_venv_cmd = ['python2', '-m', 'virtualenv', self.venv_dir]
            elif self.series in ('11.0', ):
                make_venv_cmd = ['python3', '-m', 'venv', self.venv_dir]
            else:
                self.raise_unsupported()
            subprocess.check_call(make_venv_cmd)
            self.pip_install_odoo()
            self.pip_install_odoo_autodiscover()

    def tearDown(self):
        if self.tmpd:
            shutil.rmtree(self.tmpd)

    def check_virtualenv_installed(self):
        if self.series in ('8.0', '9.0', '10.0'):
            if subprocess.call(['python2', '-c', 'import virtualenv']) != 0:
                raise RuntimeError(
                    'Please install virtualenv before running tests.')

    def raise_unsupported(self):
        raise RuntimeError("Unsupported Odoo series %s" % self.series)

    @property
    def python_exe(self):
        return opj(self.venv_dir, 'bin', 'python')

    @property
    def odoo_exe(self):
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

    @property
    def odoo_zip(self):
        return opj(self.odoo_base_dir, 'odoo-{}.zip'.format(self.series))

    def pip_install(self, *args):
        cmd = [opj(self.venv_dir, 'bin', 'pip'), 'install'] + \
            list(args)
        print('==>', cmd)
        subprocess.check_call(cmd)

    def pip_uninstall(self, *args):
        cmd = [opj(self.venv_dir, 'bin', 'pip'), 'uninstall', '-y'] + \
            list(args)
        print('==>', cmd)
        subprocess.check_call(cmd)

    def pip_install_odoo_autodiscover(self):
        self.pip_install(self.root_dir)

    def pip_install_odoo_dependencies(self):
        requirements = \
            'https://raw.githubusercontent.com/odoo/odoo/{}/' \
            'requirements.txt'.format(self.series)
        args = [
            '-f', 'https://wheelhouse.acsone.eu/manylinux1',
            '-r', requirements,
        ]
        self.pip_install(*args)

    def download_odoo(self):
        if os.path.exists(self.odoo_dir):
            return
        if not os.path.exists(self.odoo_zip):
            odoo_url = \
                'https://nightly.odoo.com/{0}/nightly/src/'\
                'odoo_{0}.latest.zip'.\
                format(self.series)
            r = requests.get(odoo_url, stream=True)
            if r.status_code == 200:
                with open(self.odoo_zip, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
        with DirectoryChanger(opj(self.odoo_base_dir)):
            subprocess.check_call(
                ['unzip', '-q', self.odoo_zip], 
                universal_newlines=True)
            dir_re = re.compile(r'^odoo-{0}c?-\d{{8}}$'.format(self.series))
            for f in os.listdir('.'):
                if dir_re.match(f) and os.path.isdir(f):
                    os.rename(f, self.odoo_dir)
                    break
            else:
                raise RuntimeError(
                    'Odoo not found in {}'.format(self.odoo_zip))

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
                [self.python_exe, '-c', 'from openerp import api'])
        elif self.series in ('10.0', ):
            subprocess.check_call(
                [self.python_exe, '-c', 'from odoo import api'])
        else:
            self.raise_unsupported()

    def pip_install_test_addon(self, name, editable):
        addon_dir = opj(self.root_dir, 'tests', 'addons', self.series, name)
        if editable:
            self.pip_install('-e', addon_dir)
        else:
            self.pip_install(addon_dir)

    def get_addons_paths(self):
        cmd = [self.odoo_exe, '--stop-after-init']
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
        for ap in addons_paths:
            if self.odoo_dir in ap:
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
        print("addons paths:", addons_paths)
        if self.editable:
            assert self._has_odoo_dir(addons_paths)
        if not not_editable_addons and self.editable:
            assert not self._has_site_packages(addons_paths)
        if not_editable_addons or not self.editable:
            assert self._has_site_packages(addons_paths)
        for addon_name in editable_addons:
            assert self._has_addon_dir(addons_paths, addon_name)


ODOO_VENV_PARAMS = [
    ('10.0', False, None),
    ('10.0', True, None),
    ('9.0', False, None),
    ('9.0', True, None),
    ('8.0', False, None),
    ('8.0', True, None),
]

ODOO_VENV_IDS = [
    '{}{}'.format(series, '-editable' if editable else '')
    for series, editable, preset_venv in ODOO_VENV_PARAMS
]

# enable this to test with an existing venv where odoo and
# odoo-autodiscover are preinstalled
if False:
    ODOO_VENV_PARAMS.append(
        ('10.0', True, '/home/sbi-local/.virtualenvs/odoo-autodiscover-test')
    )
    ODOO_VENV_IDS.append(
        '8.0:preset_venv'
    )


@pytest.fixture(scope="function", params=ODOO_VENV_PARAMS, ids=ODOO_VENV_IDS)
def odoo_venv(request):
    series, editable, preset_venv = request.param
    venv = OdooVirtualenv(series, editable, preset_venv, request.config.cache)
    try:
        venv.setUp()
    except:
        venv.tearDown()
        raise
    yield venv
    venv.tearDown()
