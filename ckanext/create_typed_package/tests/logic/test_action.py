import pytest

import ckan.tests.helpers as helpers


@pytest.mark.usefixtures("with_plugins")
class TestCtpListTypes(object):
    def test_ctp_list_types_default(self):
        types = helpers.call_action("ctp_list_types")
        assert types == ["dataset"]

    @pytest.mark.ckan_config("create_typed_package.additional_types", "first second")
    def test_ctp_list_types_include(self):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["dataset", "first", "second"]

    @pytest.mark.ckan_config("create_typed_package.additional_types", "first second")
    def test_ctp_list_types_with_default_labels(self):
        types = helpers.call_action("ctp_list_types", with_labels=True)
        assert types == [
            {"name": "dataset", "label": "dataset"},
            {"name": "first", "label": "first"},
            {"name": "second", "label": "second"},
        ]

    @pytest.mark.ckan_config("create_typed_package.label_for.dataset", "Dataset")
    @pytest.mark.ckan_config("create_typed_package.label_for.second", "#2 Dataset")
    @pytest.mark.ckan_config("create_typed_package.additional_types", "first second")
    def test_ctp_list_types_with_custom_labels(self):
        types = helpers.call_action("ctp_list_types", with_labels=True)
        assert types == [
            {"name": "second", "label": "#2 Dataset"},
            {"name": "dataset", "label": "Dataset"},
            {"name": "first", "label": "first"},
        ]

    @pytest.mark.ckan_config("create_typed_package.exclude_types", "dataset")
    def test_ctp_list_types_exclude(self):
        types = helpers.call_action("ctp_list_types")
        assert types == []

    @pytest.mark.ckan_config(
        "ckan.plugins", "create_typed_package example_idatasetform_v6"
    )
    def test_ctp_list_types_idatasetform_v6(self):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["dataset", "fancy_type"]

    @pytest.mark.ckan_config(
        "ckan.plugins",
        "create_typed_package example_idatasetform_v6 scheming_datasets",
    )
    def test_ctp_list_types_idatasetform_v6_not_using_scheming(self):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["dataset", "fancy_type"]

    @pytest.mark.ckan_config(
        "ckan.plugins",
        "create_typed_package example_idatasetform_v6 scheming_datasets",
    )
    @pytest.mark.ckan_config("create_typed_package.use_scheming", "true")
    def test_ctp_list_types_idatasetform_v6_using_scheming(self):
        types = helpers.call_action("ctp_list_types")
        assert types == []

    @pytest.mark.ckan_config("create_typed_package.use_scheming", "true")
    def test_ctp_list_types_using_disabled_scheming(self):
        types = helpers.call_action("ctp_list_types")
        assert types == []

    @pytest.mark.ckan_config("ckan.plugins", "create_typed_package scheming_datasets")
    @pytest.mark.ckan_config(
        "scheming.dataset_schemas", "ckanext.scheming:ckan_dataset.yaml"
    )
    @pytest.mark.ckan_config("create_typed_package.use_scheming", "true")
    def test_ctp_list_types_using_one_schema(self):
        types = helpers.call_action("ctp_list_types")
        assert types == ["dataset"]

    @pytest.mark.ckan_config("ckan.plugins", "create_typed_package scheming_datasets")
    @pytest.mark.ckan_config(
        "scheming.dataset_schemas",
        "ckanext.scheming:ckan_dataset.yaml ckanext.scheming:camel_photos.yaml",
    )
    @pytest.mark.ckan_config("create_typed_package.use_scheming", "true")
    def test_ctp_list_types_using_two_schemas(self):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["camel-photos", "dataset"]

    @pytest.mark.ckan_config(
        "scheming.dataset_schemas",
        "ckanext.scheming:ckan_dataset.yaml " "ckanext.scheming:camel_photos.yaml",
    )
    @pytest.mark.ckan_config("ckan.plugins", "create_typed_package scheming_datasets")
    def test_ctp_list_types_using_two_schemas_scheming_disabled(self, app):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["camel-photos", "dataset"]

    @pytest.mark.ckan_config(
        "ckan.plugins",
        "create_typed_package scheming_datasets example_idatasetform_v6",
    )
    @pytest.mark.ckan_config(
        "scheming.dataset_schemas",
        "ckanext.scheming:ckan_dataset.yaml " "ckanext.scheming:camel_photos.yaml",
    )
    def test_ctp_list_types_using_idatasetform_v6_two_schemas_not_scheming(
        self,
    ):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["camel-photos", "dataset", "fancy_type"]

    @pytest.mark.ckan_config(
        "ckan.plugins",
        "create_typed_package scheming_datasets example_idatasetform_v6",
    )
    @pytest.mark.ckan_config(
        "scheming.dataset_schemas",
        "ckanext.scheming:ckan_dataset.yaml " "ckanext.scheming:camel_photos.yaml",
    )
    @pytest.mark.ckan_config("create_typed_package.use_scheming", "true")
    def test_ctp_list_types_using_idatasetform_v6_two_schemas_scheming(
        self,
    ):
        types = helpers.call_action("ctp_list_types")
        assert sorted(types) == ["camel-photos", "dataset"]
