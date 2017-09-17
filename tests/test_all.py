#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

from __future__ import print_function


def test_odoo_auto_discover(odoo_venv):
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths()

    odoo_venv.pip_install_test_addon('a1', editable=False)
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths(
        editable_addons=[], not_editable_addons=['a1'])

    odoo_venv.pip_install_test_addon('z1', editable=False)
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths(
        editable_addons=[], not_editable_addons=['a1', 'z1'])

    odoo_venv.pip_uninstall('z1')
    odoo_venv.pip_install_test_addon('z1', editable=True)
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths(
        editable_addons=['z1'], not_editable_addons=['a1'])

    odoo_venv.pip_uninstall('a1')
    odoo_venv.pip_install_test_addon('a1', editable=True)
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths(
        editable_addons=['a1', 'z1'], not_editable_addons=[])

    odoo_venv.pip_uninstall('a1')
    odoo_venv.pip_uninstall('z1')
    odoo_venv.check_import_odoo()
    odoo_venv.check_addons_paths()
