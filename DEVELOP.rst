Development
~~~~~~~~~~~

How to run tests
----------------

To run all tests:

* ``tox`` or
* ``tox -- --capture=no --verbose`` to view progress.

To run faster tests in a preinstalled virtualenv

* create a virtualenv, and install odoo and odoo-autodiscover in it
* if you install odoo-autodiscover in editable/develop mode, symlink
  zzz_odoo_autodiscover.pth in $VIRTUAL_ENV/lib/python*/site-packages.
* the ``ODOO_AUTODISCOVER_PRESET_ENV`` to the root of your virtualenv:
  ``export ODOO_AUTODISCOVER_PRESET_ENV=$VIRTUAL_ENV``.
* then run ``tox -- --capture=no --verbose -k 10.0-preset`` (replace 10.0
  with the Odoo version you installed).

How to release
--------------

* update changelog in CHANGES.rst, referring to the next version
* python setup.py check --restructuredtext
* commit everything
* make sure tests pass!
* git tag <version>, where <version> is PEP 440 compliant
* git push --tags

Uploading of tagged versions to pypi will be taken care of by travis.
