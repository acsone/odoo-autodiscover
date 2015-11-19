# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import openerp

from . import monkey


def main():
    monkey.patch()
    openerp.cli.main()


if __name__ == "__main__":
    main()
