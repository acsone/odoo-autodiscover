# -*- coding: utf-8 -*-
# © 2017 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)


def _get_odoo_version():
    dist = __import__('pkg_resources').get_distribution('odoo')
    return dist.version


def hook(package):
    if package.__name__ == 'odoo':
        if not hasattr(package, 'cli'):
            del __import__('sys').modules['odoo']
