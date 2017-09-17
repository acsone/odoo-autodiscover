# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import setuptools
from distutils.sysconfig import get_python_lib


setuptools.setup(
    name='odoo-autodiscover',
    use_scm_version=True,
    description='An Odoo launcher that discovers addons automatically',
    long_description='\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    )),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # 'Framework :: Odoo',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Framework :: Odoo',
    ],
    license='LGPLv3',
    author='ACSONE SA/NV',
    author_email='info@acsone.eu',
    url='http://github.com/acsone/odoo-autodiscover',
    packages=[
        'odoo_autodiscover',
    ],
    install_requires=[
        # 'odoo>=8.0a,<10.1a',
        'wrapt',
    ],
    setup_requires=[
        'setuptools-scm',
    ],
    data_files=[
        (get_python_lib(prefix=''), ['zzz_odoo_autodiscover.pth']),
    ],
    scripts=[
        'odoo-autodiscover.py'
    ],
    entry_points={
        'console_scripts': [
            "odoo-server-autodiscover="
            "odoo_autodiscover.odoo_server_autodiscover:main",
            "openerp-server-autodiscover="
            "odoo_autodiscover.odoo_server_autodiscover:main",
        ],
    },
)
