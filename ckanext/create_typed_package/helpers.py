from __future__ import annotations

import ckan.plugins.toolkit as tk
from . import config


def get_helpers():
    return {
        "ctp_use_separate_route": ctp_use_separate_route,
    }


def ctp_use_separate_route():
    return config.use_separate_route()
