import pytest

import ckantoolkit as tk

import ckan.model as model
import ckan.tests.helpers as helpers
import ckan.tests.factories as factories


@pytest.mark.usefixtures("clean_db", "app", "with_plugins")
def test_ctp_list_types():
    context = {"model": model, "user": ""}
    with pytest.raises(tk.NotAuthorized):
        helpers.call_auth("ctp_list_types", context)

    user = factories.User()
    context = {"model": model, "user": user["name"]}
    assert helpers.call_auth("ctp_list_types", context)
