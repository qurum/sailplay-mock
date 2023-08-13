def token_envelope(token_dict) -> dict:
    return {
        "value": token_dict["value"],
        "pin_code": token_dict["pin_code"],
        "created_at": token_dict["created_at"],
    }


def credentials_envelope(credentials_dict) -> dict:
    return {
        "id": str(credentials_dict["_id"]),
        "store_department_key": credentials_dict["store_department_key"],
        "store_department_id": credentials_dict["store_department_id"],
        "pin_codes": credentials_dict["pin_codes"],
        "tokens": [
            token_envelope(token_dict) for token_dict in credentials_dict["tokens"]
        ],
        "created_at": credentials_dict["created_at"],
        "updated_at": credentials_dict["updated_at"],
    }


def credentials_list_envelope(credentials_dict_list) -> list:
    return [
        credentials_envelope(credentials_dict)
        for credentials_dict in credentials_dict_list
    ]
