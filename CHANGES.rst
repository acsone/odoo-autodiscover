Changes
~~~~~~~

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
