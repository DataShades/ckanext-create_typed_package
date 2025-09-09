from __future__ import annotations

import ckan.plugins.toolkit as tk

from . import config


def get_helpers():
    return {
        "ctp_use_separate_route": ctp_use_separate_route,
        "ctp_available_types": ctp_available_types,
    }


def ctp_use_separate_route():
    return config.use_separate_route()


def ctp_available_types():
    return tk.get_action("ctp_list_types")({}, {"with_labels": True})
