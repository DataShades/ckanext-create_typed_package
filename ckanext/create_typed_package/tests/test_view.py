import pytest

import ckan.tests.factories as factories


@pytest.mark.usefixtures("with_plugins")
def test_route_not_available(app):
    app.get("/dataset/select-type", status=404)


@pytest.mark.ckan_config("create_typed_package.use_separate_route", "yes")
@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_route_available(app):
    user = factories.User()
    env = {"REMOTE_USER": user["name"]}
    app.get("/dataset/select-type", environ_overrides=env, status=200)


@pytest.mark.ckan_config("create_typed_package.use_separate_route", "yes")
@pytest.mark.ckan_config("create_typed_package.route_path", "/ctp/route/path")
@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_route_available_under_custom_path(app):
    user = factories.User()
    env = {"REMOTE_USER": user["name"]}
    app.get("/dataset/select-type", environ_overrides=env, status=404)
    app.get("/ctp/route/path", environ_overrides=env, status=200)
