import ckantoolkit as tk


def get_helpers():
    return {
        "ctp_use_separate_route": ctp_use_separate_route,
    }


def ctp_use_separate_route():
    return tk.asbool(tk.config.get("create_typed_package.use_separate_route"))
