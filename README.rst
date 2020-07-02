.. image:: https://travis-ci.org/DataShades/ckanext-create_typed_package.svg?branch=master
    :target: https://travis-ci.org/DataShades/ckanext-create_typed_package

.. image:: https://codecov.io/gh/DataShades/ckanext-create_typed_package/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/DataShades/ckanext-create_typed_package

============================
ckanext-create_typed_package
============================

Add dataset type selector to the "Add dataset" button.

.. image:: https://github.com/DataShades/ckanext-create_typed_package/raw/master/selector.png

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

   # Build list of package types using ckanext-scheming API instead of
   # internal CKAN's package_type registry
   # (optional, default: false).
   create_typed_package.use_scheming = true

   # Additional types that are not are not automatically added to the
   # list for some reason
   # (optional, default: []).
   create_typed_package.additional_types = custom_type another_type

   # Package types that need to be excluded from the list of available
   # types
   # (optional, default: []).
   create_typed_package.exclude_types = custom_type another_type

   # After clicking on "Add datset" button redirect user to special
   # page with dataset type selector instead of using in-place modal
   # (optional, default: false).
   create_typed_package.use_separate_route = true

   # URL where the special page with dataset type selector will be registered.
   # (optional, default: /dataset/select-type).
   create_typed_package.route_path = /create-package/select-type
