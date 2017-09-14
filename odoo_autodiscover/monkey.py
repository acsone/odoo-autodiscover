# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import os
import subprocess
import sys

import openerp
from openerp.tools import stripped_sys_argv


_done = False


def patch():
    """ Monkey patch Odoo to discover addons from the
    odoo_addons namespace.  This method is for Odoo 8 and 9 only.
    """
    global _done
    if _done:
        return

    if openerp.release.series not in ('8.0', '9.0'):
        # nothing to do
        return

    # monkey-patch sys path for autodiscovery of addons

    initialize_sys_path_orig = openerp.modules.module.initialize_sys_path

    def initialize_sys_path_odoo_addons():
        initialize_sys_path_orig()

        ad_paths = openerp.modules.module.ad_paths

        try:
            # explicit workaround for https://github.com/pypa/pip/issues/3 and
            # https://github.com/pypa/setuptools/issues/250 (it sort of works
            # without this but I'm not sure why, so better be safe)
            __import__('pkg_resources').declare_namespace('odoo_addons')

            for ad in __import__('odoo_addons').__path__:
                ad = os.path.abspath(ad)
                if ad not in ad_paths:
                    ad_paths.append(ad)
        except ImportError:
            # odoo_addons is not provided by any distribution
            pass

    openerp.modules.module.initialize_sys_path = \
        initialize_sys_path_odoo_addons

    # monkey-patch long_polling_spawn to launch the autodiscover version

    def long_polling_spawn(self):
        nargs = stripped_sys_argv()
        cmd = nargs[0]
        cmd = os.path.join(os.path.dirname(cmd), "openerp-gevent-autodiscover")
        nargs[0] = cmd
        popen = subprocess.Popen([sys.executable] + nargs)
        self.long_polling_pid = popen.pid

    openerp.service.server.PreforkServer.long_polling_spawn = \
        long_polling_spawn

    _done = True
