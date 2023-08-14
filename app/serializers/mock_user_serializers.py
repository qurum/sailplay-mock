def user_envelope(token_dict) -> dict:
    return {
        "status": "ok",
        "phone": token_dict["user_phone"],
        "first_name": token_dict["first_name"],
        "last_name": token_dict["last_name"],
        "middle_name": token_dict["middle_name"],
        "birth_date": token_dict["birth_date"],
        "origin_user_id": token_dict["origin_user_id"],
        "id": str(token_dict["_id"]),
        "sex": token_dict["sex"],
    }
