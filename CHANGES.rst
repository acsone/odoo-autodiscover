Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

2.0.0 (2017-09-19)
------------------
- better deprecation warnings for autodiscover scripts
- improvements to setup.py and readme
- add test for Odoo 11 and python 3 where odoo-autodiscover is not necessary

2.0.0b1 (2017-09-17)
--------------------
- major rewrite: instead of adapted startup scripts that monkey patch Odoo,
  use a post import hook that automatically does the job as soon as odoo or openerp
  is imported.
- for Odoo 10 and 11, do not rely on namespace packages, but instead look for odoo/addons
  directories in PYTHONPATH 
- automated tests
- Odoo 10 support, to work around https://github.com/acsone/setuptools-odoo/issues/10
- preliminary Odoo 11 support

1.0.3 (2016-09-30)
------------------
- odoo-autodiscover is built-in Odoo 10!

1.0.2 (2016-02-06)
------------------
- [IMP] add openerp-gevent-autodiscover, and monkey patch the prefork server
  to launch that script instead of openerp-gevent.

1.0.1 (2015-12-30)
------------------
- [FIX] odoo-autodiscover.py: more reliable way to discover and import
  the official odoo.py script, so it will now work when Odoo is installed
  from the deb package

1.0.0 (2015-12-28)
------------------
- initial stable release
