from typing import Annotated

from fastapi import APIRouter, Query, Depends

from app.database import User
from app.serializers.mock_user_serializers import (
    user_envelope,
    user_info_envelope,
    user_subscriptions_envelope, user_unsubscriptions_envelope,
)

router = APIRouter()


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


async def add_user_parameters(
    user_category_name: Annotated[str | None, Query()] = None,
    first_name: Annotated[str | None, Query()] = None,
    last_name: Annotated[str | None, Query()] = None,
    middle_name: Annotated[str | None, Query()] = None,
    birth_date: Annotated[str | None, Query()] = None,
    sex: Annotated[int | str | None, Query()] = None,
):
    return {
        "user_category_name": user_category_name,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "birth_date": birth_date,
        "sex": sex,
    }


@router.get("/add")
async def add(
    user_creds: Annotated[dict, Depends(user_creds_parameters)],
    auth: Annotated[dict, Depends(token_parameters)],
    params: Annotated[dict, Depends(add_user_parameters)],
):
    for error, message in [check_user_creds(user_creds), check_token(auth)]:
        if error:
            return message

    users = find_users(
        store_department_id=auth["store_department_id"],
        user_phone=user_creds["user_phone"],
        email=user_creds["email"],
        origin_user_id=user_creds["origin_user_id"],
    )

    if len(users) != 0:
        return {
            "status": "error",
            "message": "User is already registered.User is already client.",
        }

    new_user = {}
    new_user.update(user_creds)
    new_user.update(auth)
    new_user.update(params)
    result = User.insert_one(new_user)

    return user_envelope(User.find_one({"_id": result.inserted_id}))


@router.get("/info")
async def info(
    user_creds: Annotated[dict, Depends(user_creds_parameters)],
    auth: Annotated[dict, Depends(token_parameters)],
    history: Annotated[int, Query()] = 0,
    subscriptions: Annotated[int, Query()] = 0,
):
    error, result = get_user(user_creds, auth)
    if error:
        return result
    user = result

    if history != 1:
        user.pop("history", None)

    if subscriptions != 1:
        user.pop("subscriptions", None)

    return user_info_envelope(user)


@router.get("/subscribe")
async def user_subscribe(
    user_creds: Annotated[dict, Depends(user_creds_parameters)],
    auth: Annotated[dict, Depends(token_parameters)],
    subscribe_list: Annotated[str, Query()] = "",
):
    error, result = get_user(user_creds, auth)
    if error:
        return result
    user = result
    subscribe_list = subscribe_list.split(",")
    User.find_one_and_update(
        {"_id": user["_id"]},
        {"$addToSet": {"subscriptions": {"$each": subscribe_list}}},
    )

    result = {}
    result.update(user_creds)
    result["subscribed"] = subscribe_list

    return user_subscriptions_envelope(result)


@router.get("/unsubscribe")
async def user_subscribe(
    user_creds: Annotated[dict, Depends(user_creds_parameters)],
    auth: Annotated[dict, Depends(token_parameters)],
    unsubscribe_list: Annotated[str, Query()] = "",
):
    error, result = get_user(user_creds, auth)
    if error:
        return result
    user = result
    unsubscribe_list = unsubscribe_list.split(",")
    User.find_one_and_update(
        {"_id": user["_id"]},
        {"$pull": {"subscriptions": {"$in": unsubscribe_list}}},
    )

    result = {}
    result.update(user_creds)
    result["unsubscribed"] = unsubscribe_list

    return user_unsubscriptions_envelope(result)


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
