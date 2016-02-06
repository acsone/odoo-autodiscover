# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import gevent.monkey
gevent.monkey.patch_all()  # noqa
import psycogreen.gevent
psycogreen.gevent.patch_psycopg()  # noqa

import openerp

from . import monkey


def main():
    monkey.patch()
    openerp.cli.main()


if __name__ == "__main__":
    main()
