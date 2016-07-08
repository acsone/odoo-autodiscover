odoo-autodiscover
=================

.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3
.. image:: https://badge.fury.io/py/odoo-autodiscover.svg
    :target: https://badge.fury.io/py/odoo-autodiscover

Odoo server startup scripts that discover Odoo addons
automatically without the need of the ``--addons-path`` option.
They work by looking at addons in the ``odoo_addons`` namespace
package.

This is the basic building block to package and distribute
Odoo addons using standard python infrastructure (ie
`setuptools <https://pypi.python.org/pypi/setuptools>`_,
`pip <https://pypi.python.org/pypi/pip>`_,
`wheel <https://pypi.python.org/pypi/wheel>`_,
and `pypi <https://pypi.python.org>`_).

The following thin wrappers around official Odoo startup scripts
are provided:

* ``odoo-autodiscover.py`` is the equivalent of ``odoo.py``
* ``openerp-server-autodiscover`` is the equivalent of ``openerp-server``
* ``openerp-gevent-autodiscover`` is the equivalent of ``openerp-gevent``
* ``odoo-server-autodiscover`` is an alias for ``openerp-server-autodiscover``

These scripts have exactly the same behaviour and options as their official
Odoo counterparts, except they look for additional addons by examining all
distributions providing the ``odoo_addons`` namespace package.

How to install
~~~~~~~~~~~~~~

* create a virtualenv and make sure you have a recent version of pip
  (by running ``pip install -U pip`` or using
  `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_)
* install Odoo with the standard Odoo installation procedure
* make sure Odoo is installed (the following commands must work:
  ``python -c "import openerp"``, ``odoo.py`` and ``openerp-server``,
  and ``pip list`` must show the ``odoo`` package)
* install this package (``pip install odoo-autodiscover``)

How to use
~~~~~~~~~~

* create or install odoo addons in the ``odoo_addons`` namespace package
  possibly with the help of the `setuptools-odoo
  <https://pypi.python.org/pypi/setuptools-odoo>`_ package.
* run odoo with ``openerp-server-autodiscover`` or ``odoo-autodiscover.py``
  and notice the addons path is constructued automatically

Complete example
~~~~~~~~~~~~~~~~

The following commands install Odoo 8.0 nightly, then
install ``base_import_async`` pulling all required dependencies
automatically (ie ``connector``).

It uses pre-built wheel packages for all OCA addons from https://wheelhouse.odoo-community.org.

  .. code:: Bash

    # create and activate a virtualenv
    virtualenv venv
    . ./venv/bin/activate
    # install Odoo 8.0 nightly
    pip install -r https://raw.githubusercontent.com/odoo/odoo/8.0/requirements.txt
    pip install https://nightly.odoo.com/8.0/nightly/src/odoo_8.0.latest.zip
    # install odoo-autodiscover
    pip install odoo-autodiscover
    # install base_import_async from wheelhouse.odoo-community.org
    pip install odoo-addon-base_import_async --find-links=https://wheelhouse.odoo-community.org/oca-8.0
    # start odoo
    openerp-server-autodiscover

Should you like to have an Odoo shell, simply pip install the module:

  .. code:: Bash

    pip install odoo-addon-shell --find-links=https://wheelhouse.odoo-community.org/oca-8.0
    odoo-autodiscover.py shell

To view addon packages that are installed in your virtualenv,
simply use ``pip list | grep odoo-addon-`` (note official addons
are part of the ``odoo`` package).

Technical note
~~~~~~~~~~~~~~

Since it's not possible to make ``openerp.addons`` a namespace package
(because ``openerp/__init__.py`` contains code), we use a pseudo-package named
``odoo_addons`` for the sole purpose of discovering addons installed with
setuptools in that namespace. ``odoo_addons`` is not intended to be imported
as the Odoo import hook will make sure all addons can be imported from
``openerp.addons`` as usual.

See https://pythonhosted.org/setuptools/pkg_resources.html for more
information about namespace packages.

See https://github.com/odoo/odoo/pull/8758 to follow progress with making
openerp.addons a namespace package, which will hopefully make this package
obsolete in the future.

Useful links
~~~~~~~~~~~~

* pypi page: https://pypi.python.org/pypi/odoo-autodiscover
* code repository: https://github.com/acsone/odoo-autodiscover
* report issues at: https://github.com/acsone/odoo-autodiscover/issues
* see also setuptools-odoo: https://pypi.python.org/pypi/setuptools-odoo

Credits
~~~~~~~

Author:

  * Stéphane Bidoul (`ACSONE <http://acsone.eu/>`_)

Many thanks to Daniel Reis who cleared the path, and Laurent Mignon who convinced
me it was possible to do it using standard Python setup tools and had the idea of
the odoo_addons namespace package.

