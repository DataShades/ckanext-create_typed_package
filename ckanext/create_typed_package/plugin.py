from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan import plugins as p

from ckanext.create_typed_package import helpers, views
from ckanext.create_typed_package.logic import action, auth


@tk.blanket.config_declarations
class CreateTypedPackagePlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IBlueprint)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "create_typed_package")

    # IActions

    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions

    def get_auth_functions(self):
        return auth.get_auth_functions()

    # IBlueprint

    def get_blueprint(self):
        if tk.h.ctp_use_separate_route():
            return views.get_blueprints()
        return []

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()
