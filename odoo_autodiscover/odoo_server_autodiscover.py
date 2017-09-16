# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import sys
import warnings

import openerp


def main():
    warnings.warn('%s is deprecated; please run odoo normally.' % sys.argv[0])
    openerp.cli.main()


if __name__ == "__main__":
    main()
