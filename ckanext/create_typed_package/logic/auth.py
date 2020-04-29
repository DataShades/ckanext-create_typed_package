# -*- coding: utf-8 -*-

import ckantoolkit as tk


def get_auth_functions():
    return {
        "ctp_list_types": ctp_list_types,
    }


@tk.auth_allow_anonymous_access
def ctp_list_types(context, data_dict=None):

    tk.check_access("package_create", context, data_dict)
    return {"success": True}
