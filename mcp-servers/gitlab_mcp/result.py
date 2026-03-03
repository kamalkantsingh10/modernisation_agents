def make_result(data=None, flags=None, message="", status="ok"):
    return {
        "status": status,
        "data": data,
        "flags": flags or [],
        "message": message,
    }


def make_error(message, flags=None):
    return make_result(status="error", message=message, flags=flags)


def make_warning(data, message, flags=None):
    return make_result(status="warning", data=data, message=message, flags=flags)
