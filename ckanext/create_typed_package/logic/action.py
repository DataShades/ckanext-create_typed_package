from __future__ import annotations

from operator import itemgetter

from typing import Any
from ckan import types
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.plugins as lib_plugins
from ckanext.create_typed_package import config

CONFIG_LABEL_PREFIX = "create_typed_package.label_for."

default_sorter = itemgetter("label")


def get_actions() -> dict[str, Any]:
    return {
        "ctp_list_types": ctp_list_types,
    }


def _labels_from_config() -> dict[str, str]:
    labels: dict[str, str] = {}
    for option, value in tk.config.items():
        if not option.startswith(CONFIG_LABEL_PREFIX):
            continue
        labels[option[len(CONFIG_LABEL_PREFIX) :]] = value
    return labels


@tk.side_effect_free
def ctp_list_types(context: types.Context, data_dict: dict[str, Any]):
    with_labels = tk.asbool(data_dict.get("with_labels"))

    tk.check_access("ctp_list_types", context, data_dict)

    dt = _get_scheming_types() if _use_scheming() else _get_native_types()
    result = list(set(dt).union(_additional_types()).difference(_exclude_types()))

    if with_labels:
        labels = _labels_from_config()
        sorter = config.sorter()
        result = sorted(
            [{"name": t, "label": labels.get(t) or tk._(t)} for t in result],
            key=sorter,
        )
    return result


def _get_native_types():
    return list(lib_plugins._package_plugins) + ["dataset"]  # pyright: ignore[reportPrivateUsage]


def _get_scheming_types() -> list[str]:
    if not p.plugin_loaded("scheming_datasets"):
        return []
    return tk.get_action("scheming_dataset_schema_list")({}, {})


def _use_scheming():
    return config.use_scheming()


def _additional_types():
    return config.additional_types()


def _exclude_types():
    return config.exclude_types()
