from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk

from . import config


def get_helpers():
    return {
        "ctp_use_separate_route": ctp_use_separate_route,
        "ctp_available_types": ctp_available_types,
    }


def ctp_use_separate_route():
    return config.use_separate_route()


def ctp_available_types() -> list[dict[str, Any]]:
    try:
        return tk.get_action("ctp_list_types")({}, {"with_labels": True})
    except tk.NotAuthorized:
        return []
