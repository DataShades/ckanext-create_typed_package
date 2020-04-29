import ckan.plugins as plugins
import ckantoolkit as tk

import ckanext.create_typed_package.logic.action as action
import ckanext.create_typed_package.logic.auth as auth
import ckanext.create_typed_package.views as views
import ckanext.create_typed_package.helpers as helpers


class CreateTypedPackagePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

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
