# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import os
import openerp
from openerp.tools.parse_version import parse_version


def patch():
    """ Monkey patch Odoo to discover addons from the odoo_addons namespace """
    version = openerp.cli.server.__version__
    if parse_version(version) < parse_version('8.0'):
        raise RuntimeError("Unsupported Odoo version %s" % version)

    initialize_sys_path_orig = openerp.modules.module.initialize_sys_path

    def initialize_sys_path_odoo_addons():
        initialize_sys_path_orig()

        ad_paths = openerp.modules.module.ad_paths

        try:
            for ad in __import__('odoo_addons').__path__:
                ad = os.path.abspath(ad)
                if ad not in ad_paths:
                    ad_paths.append(ad)
        except ImportError:
            # odoo_addons is not provided by any distribution
            pass

    openerp.modules.module.initialize_sys_path = initialize_sys_path_odoo_addons
