from __future__ import annotations

from operator import itemgetter

import ckan.plugins as p

import ckan.plugins.toolkit as tk

from ckanext.create_typed_package import config


CONFIG_LABEL_PREFIX = "create_typed_package.label_for."

default_sorter = itemgetter("label")


def get_actions():
    return {
        "ctp_list_types": ctp_list_types,
    }


def _labels_from_config():
    labels = {}
    for option, value in tk.config.items():
        if not option.startswith(CONFIG_LABEL_PREFIX):
            continue
        labels[option[len(CONFIG_LABEL_PREFIX) :]] = value
    return labels


@tk.side_effect_free
def ctp_list_types(context, data_dict):
    with_labels = tk.asbool(data_dict.get("with_labels"))

    tk.check_access("ctp_list_types", context, data_dict)
    if _use_scheming():
        types = _get_scheming_types()
    else:
        types = _get_native_types()
    result = list(set(types).union(_additional_types()).difference(_exclude_types()))

    if with_labels:
        labels = _labels_from_config()
        sorter = config.sorter()
        result = sorted(
            [{"name": t, "label": labels.get(t) or tk._(t)} for t in result],
            key=sorter,
        )
    return result


def _get_native_types():
    from ckan.lib.plugins import _package_plugins

    return list(_package_plugins) + ["dataset"]


def _get_scheming_types():
    if not p.plugin_loaded("scheming_datasets"):
        return []
    return tk.get_action("scheming_dataset_schema_list")({}, {})


def _use_scheming():
    return config.use_scheming()


def _additional_types():
    return config.additional_types()


def _exclude_types():
    return config.exclude_types()
