odoo-autodiscover
=================

.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3
.. image:: https://badge.fury.io/py/odoo-autodiscover.svg
    :target: https://badge.fury.io/py/odoo-autodiscover
.. image:: https://travis-ci.org/acsone/odoo-autodiscover.svg?branch=master
   :target: https://travis-ci.org/acsone/odoo-autodiscover

Enhance Odoo to automatically discover available addons without the need of 
the ``--addons-path`` option.

For Odoo 8 and 9, it works by looking at addons in the 
``odoo_addons`` namespace package. For Odoo 10 and 11, it
works by looking for ``odoo/addons`` directories in PYTHONPATH.

Addons that install this way can be packaged with the help of
`setuptools-odoo <https://pypi.python.org/pypi/setuptools-odoo>`_.

How to install
~~~~~~~~~~~~~~

* Create a virtualenv and make sure you have a recent version of pip
  (by running ``pip install -U pip`` or using
  `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_).
* Install Odoo in your virtualenv with the standard Odoo installation procedure
  (a good way is to run ``pip install -e .`` from the Odoo root directory).
* Make sure Odoo is installed correctly:

  * ``pip list`` must show ``odoo``.
  * for Odoo 8 and 9, running ``python -c "import openerp.api"`` 
    and ``openerp-server`` must work
  * for Odoo 10 and 11, running ``python -c "import odoo.api"`` 
    and ``odoo`` must work 

* Install this package (``pip install odoo-autodiscover``).

How to use
~~~~~~~~~~

* Create and/or install odoo addons in the ``odoo/addons`` namespace (for Odoo 10 and 11) 
  or the ``odoo_addons`` namespace (for Odoo 8 and 9),
  possibly with the help of the `setuptools-odoo
  <https://pypi.python.org/pypi/setuptools-odoo>`_ package.
* Run odoo as usual and notice the addons path is extended automatically.

Complete example
~~~~~~~~~~~~~~~~

The following commands install Odoo 8.0 nightly, then
install ``base_import_async`` pulling all required dependencies
automatically (ie ``connector``).

It uses pre-built wheel packages for OCA addons from pypi.

  .. code:: Bash

    # create and activate a virtualenv
    virtualenv venv
    . ./venv/bin/activate
    # install Odoo 8.0 nightly
    pip install -r https://raw.githubusercontent.com/odoo/odoo/8.0/requirements.txt
    pip install https://nightly.odoo.com/8.0/nightly/src/odoo_8.0.latest.zip
    # install odoo-autodiscover
    pip install odoo-autodiscover
    # install base_import_async from pypi
    pip install odoo8-addon-base_import_async --pre
    # start odoo
    openerp-server

At this point, you should see in the Odoo log that the site-packages directory appears in the addons path.

You can easily install additional addons. For example, should you like to have an Odoo 8 shell, 
using the OCA shell module, simply pip install the module:

  .. code:: Bash

    pip install odoo8-addon-shell
    openerp-server shell

To view addon packages that are installed in your virtualenv,
simply use ``pip list | grep odoo<8|9|10>-addon-`` (note official addons
are part of the ``odoo`` package).

Technical notes
~~~~~~~~~~~~~~~

With Odoo 8 and 9 it's not possible to make ``openerp.addons`` a namespace package
(because ``openerp/__init__.py`` contains code), we use a pseudo-package named
``odoo_addons`` for the sole purpose of discovering addons installed with
setuptools in that namespace. ``odoo_addons`` is not intended to be imported
as the Odoo import hook will make sure all addons can be imported from
``openerp.addons`` as usual.

With Odoo 10, we attempted to use pkg_resource style namespace packages.
It worked fine until setuptools 31, at which point we had to cope with
https://github.com/acsone/setuptools-odoo/issues/10. Hence the workaround
in ``odoo-autodiscover`` 2.0.

For Odoo 11 under Python 3, we hope we can make ``odoo-autodiscover`` obsolete
again, this is the purpose of https://github.com/odoo/odoo/pull/19517.

See https://packaging.python.org/guides/packaging-namespace-packages/ for more
information about namespace packages.

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
