# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)


def hook(package):
    if package.__name__ == 'odoo':
        if not hasattr(package, 'api'):
            # work around https://github.com/acsone/setuptools-odoo/issues/10
            # Since 'api' is not in the odoo package, it means
            # odoo/__init__.py did not run, so what we have here is a dummy
            # odoo package created by setuptools' *-nspkg.pth files.
            # This hook runs after all *-nspkg.pth files because it is named
            # zzz_ and .pth file run in alphabetical order.
            # We remove it so 'import odoo' that will be done in the actual
            # main program will have a chance to run odoo/__init__.py, which
            # in turn will run odoo/addons/__init__.py which will run
            # declare_namespace('odoo.addons') which will rediscover all the
            # parts of the odoo.addons namespace.
            del __import__('sys').modules['odoo']
    elif package.__name__ == 'openerp':
        # automatic monkey patch after importing openerp 8/9
        try:
            from . import monkey
        except:
            # this happens when the hook triggers while importing monkey
            # ie when the *autodiscover scripts are run
            pass
        else:
            monkey.patch()
