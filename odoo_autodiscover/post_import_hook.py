# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import os
import sys


def hook_odoo(package):
    """ work around Odoo 10 issue
    https://github.com/acsone/setuptools-odoo/issues/10

    # This hook should runs after all *-nspkg.pth files because it is named
    # zzz_ and .pth file run in alphabetical order.
    """
    if sys.version_info.major != 2:
        return
    if package.__name__ == 'odoo':
        if not hasattr(package, 'release'):
            # Since 'release' is not in the odoo package, it means
            # odoo/__init__.py did not run, so what we have here is a dummy
            # odoo package created by setuptools' *-nspkg.pth files.
            # We remove it so 'import odoo' that will be done in the actual
            # main program will have a chance to run odoo/__init__.py.
            if 'odoo.addons' in sys.modules:
                del sys.modules['odoo.addons']
            if 'odoo' in sys.modules:
                del sys.modules['odoo']


def hook_odoo_modules(package):
    if package.__name__ == 'odoo.modules':
        ad_paths = package.module.ad_paths
        for p in sys.path:
            ad = os.path.abspath(os.path.join(p, 'odoo', 'addons'))
            if os.path.isdir(ad):
                if ad not in ad_paths:
                    ad_paths.append(ad)


def hook_openerp_modules(package):
    if package.__name__ == 'openerp.modules':
        try:
            ad_paths = package.module.ad_paths
            for p in __import__('odoo_addons').__path__:
                ad = os.path.abspath(p)
                if os.path.isdir(ad):
                    if ad not in ad_paths:
                        ad_paths.append(ad)
        except ImportError:
            # no distribution provides odoo_addons
            pass
