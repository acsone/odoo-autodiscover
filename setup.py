# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import setuptools


setuptools.setup(
    name='odoo-autodiscover',
    version='0.5.0',
    description='An Odoo launcher that discovers addons automatically',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Odoo',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
            'GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    license='LGPLv3',
    author='ACSONE SA/NV',
    author_email='info@acsone.eu',
    url='http://github.com/acsone/odoo-autodiscover',
    packages=[
        'odoo_autodiscover',
    ],
    install_requires=[
        'odoo>=8',
    ],
    scripts=['odoo-autodiscover.py'],
    entry_points={
        'console_scripts': [
            "odoo-server-autodiscover="
            "odoo_autodiscover.odoo_server_autodiscover:main",
            "openerp-server-autodiscover="
            "odoo_autodiscover.odoo_server_autodiscover:main",
        ],
    },
)
