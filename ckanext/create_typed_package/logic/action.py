# -*- coding: utf-8 -*-

from operator import itemgetter
from werkzeug.utils import import_string

import ckan.plugins as p
import ckantoolkit as tk

CONFIG_LABEL_PREFIX = "create_typed_package.label_for."

CONFIG_LABEL_SORTER = "create_typed_package.sorter"
DEFAULT_LABEL_SORTER = "ckanext.create_typed_package.logic.action:default_sorter"

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
        sorter = import_string(tk.config.get(CONFIG_LABEL_SORTER, DEFAULT_LABEL_SORTER))
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
    return tk.get_action("scheming_dataset_schema_list")(None, {})


def _use_scheming():
    return tk.asbool(tk.config.get("create_typed_package.use_scheming"))


def _additional_types():
    return tk.aslist(tk.config.get("create_typed_package.additional_types"))


def _exclude_types():
    return tk.aslist(tk.config.get("create_typed_package.exclude_types"))
