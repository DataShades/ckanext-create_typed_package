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


## Usage

This plugin adds a widget/page for selecting dataset type when user trying to
create the new dataset. Note, the plugin itself does not register any custom
dataset types neither it introduces any tools for registering dataset types. It
means, you need to create multiple dataset types manually before using this
plugin. Check [CKAN
documentation](https://docs.ckan.org/en/2.11/extensions/remote-config-update.html)
or [ckanext-scheming](https://github.com/ckan/ckanext-scheming) if you don't
know how to create dataset types.

For simplicity, we'll use ckanext-scheming in this guide. Assuming you don't
have any custom dataset types, let's create them right now. First, install
ckanext-scheming:

```sh
pip install ckanext-scheming
```

Then add `scheming_datasets` to the list of enabled plugins, alongside with
`create_typed_package`:

```ini
ckan.plugins = scheming_datasets create_typed_package
```

And now enable in the CKAN config file three custom dataset types that are used
by the current extension for tests:

```ini
scheming.dataset_schemas =
                         ckanext.create_typed_package.tests:schemas/first.yaml
                         ckanext.create_typed_package.tests:schemas/second.yaml
                         ckanext.create_typed_package.tests:schemas/third.yaml
```

Restart CKAN. Because of custom datset types, apart from the standard dataset
listing available at `/dataset/`, you also have 3 new endpoints, one per custom
dataset type:

* `/first-type`
  ![First type listing](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/first-type-listing.png)
* `/second-type`
  ![First type listing](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/second-type-listing.png)

* `/third-type`
  ![Third type listing](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/third-type-listing.png)


On every custom page you can click **Add ???-type** and dataset creation form
with corresponding metadata fields will be rendered.

![First type form](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/first-type-form.png)

But if you go back to main `/dataset` page and click **Add dataset** there,
you'll see the modal where you can select the exact type you want to create:

![Selector inside modal](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/modal.png)

That's the main feature provided by the current plugin.

Note, if you don't see the modal, check the JavaScript console for errors. If
you see no errors or cannot fix them, thre is an alternative way.

Modify the templates and add linkg to `/dataset/select-type`. This page does
not exist yet and in order to fix it, add
`create_typed_package.use_separate_route = true` to the CKAN config file. Then
reload the application and now you'll see dataset type selector on this new
route.

![Selector on separate page](https://github.com/DataShades/ckanext-create_typed_package/raw/master/img/separate-route.png)

This method is more predictable but it requires modification of templates,
that's why modal is chosen as a default.

### Dynamic options

If you need to show different options for different pages, for example, only
type A1 and A2 for organization AAA, only type B1 and B2 for organization BBB,
etc, you need to add [chained
action](https://docs.ckan.org/en/2.11/extensions/plugins-toolkit.html#ckan.plugins.toolkit.ckan.plugins.toolkit.chained_action)
`ctp_list_types`.

In your own extension that implements
[IAction](https://docs.ckan.org/en/2.11/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IActions)
interface, register action `ctp_list_types` with the following code:

```py
import ckan.plugins.toolkit as tk
from ckan.types import Context

@tk.chained_action
@tk.side_effect_free
def ctp_list_types(next_action: Any, context: Context, data_dict: dict[str, Any]):

    if tk.get_endpoint() == ("organization", "read"):
        organization_id = tk.request.view_args.id
        allowed_types = ... # compute types depending on organization_id

        return [
            {"name": item.VALUE, "label": item.LABEL}
            for item in allowed_types
        ]

    return next_action(context, data_dict)
```

Here we check current endpoint using `tk.get_endpoint()`. If we are on the
organization page, instead of all available types we return only subset of
`allowed_types`. Note, response must be in format of list that contains
dictionaries with `name`(actual dataset type) and `label`(human readable label
for `select` tag). If action returns more than one item, user sees a modal upon
clicking **Add Dataset**. If action returns *exactly* one item, user is
redirected to the corresponding form immediately after the click on **Add
Dataset**.

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
