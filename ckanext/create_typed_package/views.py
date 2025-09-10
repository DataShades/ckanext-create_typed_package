from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk

from . import config


def get_blueprints():
    ctp = Blueprint("create_typed_package", __name__)
    path = config.route_path()

    ctp.add_url_rule(path, view_func=SelectDatasetTypeView.as_view("select_dataset_type"))
    return [ctp]


class SelectDatasetTypeView(MethodView):
    def _redirect(self, type: str):
        return tk.redirect_to(type + ".new", **tk.request.args.to_dict(False))

    def post(self):
        return self._redirect(tk.request.form["type"])

    def get(self):
        types = tk.get_action("ctp_list_types")({"user": tk.c.user}, {"with_labels": True})

        if len(types) == 1:
            return self._redirect(types[0]["name"])

        extra_vars = {
            "form_snippet": "package/snippets/ctp_select_dataset_type_form.html",
            "pkg_dict": {},
            "form_vars": {"package_types": [{"value": t["name"], "text": t["label"]} for t in types]},
        }
        return tk.render("package/ctp_select_dataset_type.html", extra_vars)
