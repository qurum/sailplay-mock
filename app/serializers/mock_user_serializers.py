def user_envelope(user_dict) -> dict:
    return {
        "status": "ok",
        "phone": user_dict.get("user_phone", ""),
        "first_name": user_dict.get("first_name", ""),
        "last_name": user_dict.get("last_name", ""),
        "middle_name": user_dict.get("middle_name", ""),
        "birth_date": user_dict.get("birth_date", ""),
        "origin_user_id": user_dict.get("origin_user_id", ""),
        "id": str(user_dict.get("_id")),
        "sex": user_dict.get("sex", ""),
    }


def history_envelope(token_dict) -> dict:
    return {
        "action": token_dict.get("action", ""),
        "action_date": token_dict.get("action_date", ""),
        "is_completed": token_dict.get("is_completed", ""),
        "points_delta": token_dict.get("points_delta", ""),
        "name": token_dict.get("name", ""),
    }


def user_info_envelope(user_info_dict) -> dict:
    result = {
        "category": user_info_dict.get("category", ""),
        "status": "ok",
        "origin_user_id": user_info_dict.get("origin_user_id", ""),
        "first_name": user_info_dict.get("first_name", ""),
        "last_name": user_info_dict.get("last_name", ""),
        "middle_name": user_info_dict.get("middle_name", ""),
        "sex": user_info_dict.get("sex", ""),
        "phone": user_info_dict.get("user_phone", ""),
        "points": [],
        "email": user_info_dict.get("email", ""),
        "birth_date": user_info_dict.get("birth_date", ""),
        "id": str(user_info_dict.get("_id", "")),
        "user_points": user_info_dict.get("user_points", ""),
        "message": "",
        "media_url": "",
        "available_gifts": user_info_dict.get("available_gifts", ""),
        "over_user_points_gifts": user_info_dict.get("over_user_points_gifts", ""),
    }

    if user_info_dict.get("history", None):
        result["history"] = [
            history_envelope(hr) for hr in user_info_dict.get("history", "")
        ]

    if user_info_dict.get("subscriptions", None):
        result["subscriptions"] = user_info_dict.get("subscriptions")

    return result


def user_subscriptions_envelope(subscriptions_dict) -> dict:
    return {
        "status": "ok",
        "user": {
            "origin_user_id": subscriptions_dict.get("origin_user_id", ""),
            "phone": subscriptions_dict.get("user_phone", ""),
            "email": subscriptions_dict.get("email", ""),
        },
        "subscribed": subscriptions_dict.get("subscribed", []),
    }


def user_unsubscriptions_envelope(subscriptions_dict) -> dict:
    return {
        "status": "ok",
        "user": {
            "origin_user_id": subscriptions_dict.get("origin_user_id", ""),
            "phone": subscriptions_dict.get("user_phone", ""),
            "email": subscriptions_dict.get("email", ""),
        },
        "unsubscribed": subscriptions_dict.get("unsubscribed", []),
    }
