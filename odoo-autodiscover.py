#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import imp
import sys
from distutils.spawn import find_executable

from odoo_autodiscover import monkey


def main():
    odoo_py = find_executable('odoo.py')
    if not odoo_py:
        sys.stderr.write('The odoo.py executable could not be found, '
                         'therefore odoo-autodiscover.py can not start.\n')
        sys.exit(1)
    odoo = imp.load_source('odoo', odoo_py)
    monkey.patch()
    odoo.main()


if __name__ == "__main__":
    main()
