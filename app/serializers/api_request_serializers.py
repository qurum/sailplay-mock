def api_request_envelope(api_request) -> dict:
    return {
        "method": api_request["method"],
        "route": api_request["route"],
        "headers": api_request["headers"],
        "body": api_request["body"],
        "host": api_request["host"],
        "created_at": api_request["created_at"],
        "updated_at": api_request["updated_at"],
    }


def api_request_list_envelope(api_request_list) -> list:
    return [api_request_envelope(api_request) for api_request in api_request_list]
