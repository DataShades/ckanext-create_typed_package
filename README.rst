.. image:: https://travis-ci.org/DataShades/ckanext-create_typed_package.svg?branch=master
    :target: https://travis-ci.org/DataShades/ckanext-create_typed_package

.. image:: https://codecov.io/gh/DataShades/ckanext-create_typed_package/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/DataShades/ckanext-create_typed_package

============================
ckanext-create_typed_package
============================

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-create_typed_package:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-create_typed_package Python package into your virtual environment::

     pip install ckanext-create-typed-package

3. Add ``create_typed_package`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/ckan.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config settings
---------------

::

   # The minimum number of hours to wait before re-checking a resource
   # (optional, default: false).
   create_typed_package.use_scheming = true

   # The minimum number of hours to wait before re-checking a resource
   # (optional, default: []).
   create_typed_package.additional_types = custom_type another_type

   # The minimum number of hours to wait before re-checking a resource
   # (optional, default: []).
   create_typed_package.exclude_types = custom_type another_type

   # The minimum number of hours to wait before re-checking a resource
   # (optional, default: false).
   create_typed_package.use_separate_route = true

   # The minimum number of hours to wait before re-checking a resource
   # (optional, default: /dataset/select-type).
   create_typed_package.route_path = /create-package/select-type

----------------------
Developer installation
----------------------

To install ckanext-create_typed_package for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/DataShades/ckanext-create_typed_package.git
    cd ckanext-create_typed_package
    python setup.py develop


-----
Tests
-----

To run the tests, do::

    pytest --ckan-ini=test.ini

To run the tests and produce a coverage report, first make sure you have
``pytest-cov`` installed in your virtualenv (``pip install pytest-cov``) then run::

    pytest --ckan-ini=test.ini  --cov=ckanext.create_typed_package
