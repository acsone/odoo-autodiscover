Odoo Autodiscover
=================

Odoo server startup scripts that discover Odoo addons
automatically without the need of the --addons-path option.

It works by looking at addons in the odoo_addons namespace
package.

The following scripts are provided by this package:
* odoo-autodiscover.py is the equivalent of the odoo.py script
* openerp-server-autodiscover is the equivalent of openerp-server
* odoo-server-autodiscover is an alias for openerp-server-autodiscover

These scripts have exactly the same behaviour and options than
their standard Odoo counterpart, except the look for addons
by examining all distributions providing the odoo_addons namespace
package.

How to install
--------------

* create a virtualenv
* install Odoo with the standard Odoo installation procedure
* make sure odoo is installed (the following commands must work:
  python -c "import openerp", odoo.py and openerp-server)
* install this package (pip install odoo-autodiscover)

How to use
----------

* create or install odoo addons in the odoo_addons namespace package
  possibly with the help of the setuptools-odoo package
* run odoo with openerp-server-autodiscover or odoo-autodiscover.py
  and notice the addons path is constructued automatically

Technical note
--------------

Since it's not possible to make openerp.addons a namespace package
(because openerp/__init__.py contains code), we use a pseudo-package named
odoo_addons for the sole purpose of discovering addons installed with
setuptools in that namespace. odoo_addons is not intended to be imported
as the Odoo import hook will make sure all addons can be imported from
openerp.addons.

See https://pythonhosted.org/setuptools/pkg_resources.html for more
information about namespace packages.

See https://github.com/odoo/odoo/pull/8758 to follow progress with making
openerp.addons a namespace package, which will hopefully make this package
obsolete in the future.

Credits
-------

Author:

  * Stéphane Bidoul (ACSONE)
