def login_ok_envelope(login_dict) -> dict:
    return {
        "status": login_dict["status"],
        "token": login_dict["token"],
        "pin_codes": login_dict["pin_codes"],
    }


def login_error_envelope(login_dict) -> dict:
    return {"status": login_dict["status"], "message": login_dict["message"]}
