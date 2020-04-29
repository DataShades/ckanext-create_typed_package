#!/bin/sh -e
set -ex

pytest --ckan-ini=subdir/test.ini --cov=ckanext.create_typed_package ckanext/create_typed_package/tests
