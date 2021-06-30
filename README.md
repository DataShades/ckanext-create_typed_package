[![Tests](https://github.com/DataShades/ckanext-create_typed_package/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/DataShades/ckanext-create_typed_package/actions)

# ckanext-create_typed_package


Add dataset type selector to the "Add dataset" button.

![Preview](https://github.com/DataShades/ckanext-create_typed_package/raw/master/selector.png)


## Installation

To install ckanext-create_typed_package:

1. Install the ckanext-create_typed_package Python package

		pip install ckanext-create-typed-package

1. Add ``create_typed_package`` to the ``ckan.plugins`` setting in your CKAN
   config file.


## Config settings

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

	# Custom label for dataset type. It will be used by `ctp_list_types`
	# action and, as result, by the type-picker UI widget. Labels provided in a
	# form `create_typed_package.label_for.<TYPE>`, where machine-name for a type
	# is used instead of `<TYPE>`.
	# (optional, default: tk._(type_machine_name)).
	create_typed_package.label_for.dataset = Publication
