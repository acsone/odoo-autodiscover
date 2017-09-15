# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import sys


_odoo_addons_path = set()


def hook_odoo(package):
    """ work around
    https://github.com/acsone/setuptools-odoo/issues/10

    # This hook runs after all *-nspkg.pth files because it is named
    # zzz_ and .pth file run in alphabetical order.
    """
    # TODO: find a way to run this for Odoo 10.0 only
    if package.__name__ == 'odoo':
        if not hasattr(package, 'release'):
            # Since 'release' is not in the odoo package, it means
            # odoo/__init__.py did not run, so what we have here is a dummy
            # odoo package created by setuptools' *-nspkg.pth files.
            # We remove it so 'import odoo' that will be done in the actual
            # main program will have a chance to run odoo/__init__.py.
            # We preserve the __path__ of odoo.addons to restore it
            # after odoo/__init__.py has run.
            if 'odoo.addons' in sys.modules:
                _odoo_addons_path.update(sys.modules['odoo.addons'].__path__)
                del sys.modules['odoo.addons']
            if 'odoo' in sys.modules:
                del sys.modules['odoo']
    elif package.__name__ == 'odoo.release':
        # here we are sure odoo/__init__.py has run
        # we restore odoo.addons.__path__
        if 'odoo.addons' in sys.modules:
            _odoo_addons_path.update(sys.modules['odoo.addons'].__path__)
            sys.modules['odoo.addons'].__path__[:] = list(_odoo_addons_path)


def hook_openerp(package):
    """ automatic monkey patch for Odoo 8 and 9 """
    if package.__name__ == 'openerp':
        try:
            from . import monkey
        except ImportError:
            # this happens when the hook triggers while importing monkey
            # ie when the *autodiscover scripts are run
            pass
        else:
            monkey.patch()
