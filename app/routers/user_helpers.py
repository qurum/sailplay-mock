from typing import Annotated

from fastapi import Query

from app.database import User


async def token_parameters(
    token: Annotated[str | None, Query()] = None,
    store_department_id: Annotated[int | str | None, Query()] = None,
):
    return {
        "token": token,
        "store_department_id": store_department_id,
    }


async def user_creds_parameters(
    user_phone: Annotated[int | str | None, Query()] = None,
    email: Annotated[str | None, Query()] = None,
    origin_user_id: Annotated[int | str | None, Query()] = None,
):
    return {
        "user_phone": user_phone,
        "email": email,
        "origin_user_id": origin_user_id,
    }


def check_user_creds(user_creds):
    if (
        not user_creds["user_phone"]
        and not user_creds["email"]
        and not user_creds["origin_user_id"]
    ):
        return (
            True,
            {
                "status": "error",
                "message": "Provide user_phone or email or origin_user_id",
            },
        )
    return False, ""


def check_token(token_params):
    if not token_params["token"]:
        return (
            True,
            {
                "status": "error",
                "message": "Provide token",
            },
        )

    if not token_params["store_department_id"]:
        return (
            True,
            {
                "status": "error",
                "message": "Provide store_department_id",
            },
        )
    return False, ""


def get_user(user_creds, auth):
    for error, message in [check_user_creds(user_creds), check_token(auth)]:
        if error:
            return (True, message)

    users = find_users(
        store_department_id=auth["store_department_id"],
        user_phone=user_creds["user_phone"],
        email=user_creds["email"],
        origin_user_id=user_creds["origin_user_id"],
    )

    if len(users) == 0:
        return (True, {"status": "error", "message": "User does not exist."})

    user = dict(users[0])

    return False, user


def find_users(
    store_department_id,
    user_phone=None,
    email=None,
    origin_user_id=None,
):
    query = []

    if user_phone:
        query.append({"user_phone": user_phone})

    if email:
        query.append({"email": email})

    if origin_user_id:
        query.append({"origin_user_id": origin_user_id})

    pipeline = [
        {
            "$match": {
                "$and": [
                    {"$or": query},
                    {"store_department_id": store_department_id},
                ]
            },
        }
    ]

    return list(User.aggregate(pipeline))
