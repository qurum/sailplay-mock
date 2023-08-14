def points_add_envelope(points_add_dict) -> dict:
    return {
        "status": "ok",
        "points": points_add_dict.get("points", 0),
        "public_key": "",
        "receipt_date": str(points_add_dict["receipt_date"]),
    }
