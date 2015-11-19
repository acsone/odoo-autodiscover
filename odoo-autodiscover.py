# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

# this imports the odoo.py script (not completely clean, but there is no other
# way due to the way the upstream script is packaged)
import odoo

from odoo_autodiscover import monkey


def main():
    monkey.patch()
    odoo.main()


if __name__ == "__main__":
    main()
