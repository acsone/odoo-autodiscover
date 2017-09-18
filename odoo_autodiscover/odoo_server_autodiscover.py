# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import os
import sys


def main():
    sys.stderr.write('The {} script is deprecated. '
                     'Please use the usual openerp-server. '
                     'As long as odoo-autodiscover is installed, '
                     'everything should work.\n'.
                     format(os.path.basename(sys.argv[0])))
    try:
        import openerp
    except ImportError:
        sys.stderr.write('Error importing openerp. Make sure Odoo 8 or 9 '
                         'is installed.\n')
        raise
    openerp.cli.main()


if __name__ == "__main__":
    main()
