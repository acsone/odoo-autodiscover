How to release
==============

* update version in setup.py
* update changelog in CHANGES.rst
* python setup.py check --restructuredtext
* commit everything
* git tag <version>
* git push --tags
* python setup.py sdist bdist_wheel
* twine upload
