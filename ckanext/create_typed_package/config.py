from __future__ import annotations
from typing import Any, Callable
import ckan.plugins.toolkit as tk
from werkzeug.utils import import_string


ROUTE_PATH = "create_typed_package.route_path"
USE_SEPARATE_ROUTE = "create_typed_package.use_separate_route"

USE_SCHEMING = "create_typed_package.use_scheming"
ADDITIONAL_TYPES = "create_typed_package.additional_types"
EXCLUDE_TYPES = "create_typed_package.exclude_types"
SORTER = "create_typed_package.sorter"


def route_path() -> str:
    return tk.config[ROUTE_PATH]


def use_separate_route() -> bool:
    return tk.config[USE_SEPARATE_ROUTE]


def use_scheming() -> bool:
    return tk.config[USE_SCHEMING]


def additional_types() -> list[str]:
    return tk.config[ADDITIONAL_TYPES]


def exclude_types() -> list[str]:
    return tk.config[EXCLUDE_TYPES]


def sorter() -> Callable[[Any], Any]:
    return import_string(tk.config[SORTER])
