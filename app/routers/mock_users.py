from typing import Annotated

from fastapi import APIRouter, Query, Depends

from app.database import User
from app.serializers.mock_user_serializers import user_envelope

router = APIRouter()


async def add_user_parameters(
        user_phone: Annotated[int | str | None, Query()] = None,
        email: Annotated[str | None, Query()] = None,
        origin_user_id: Annotated[int | str | None, Query()] = None,
        token: Annotated[str | None, Query()] = None,
        store_department_id: Annotated[int | str | None, Query()] = None,
        user_category_name: Annotated[str | None, Query()] = None,
        first_name: Annotated[str | None, Query()] = None,
        last_name: Annotated[str | None, Query()] = None,
        middle_name: Annotated[str | None, Query()] = None,
        birth_date: Annotated[str | None, Query()] = None,
        sex: Annotated[int | str | None, Query()] = None,
):
    return {
        "user_phone": user_phone,
        "email": email,
        "origin_user_id": origin_user_id,
        "token": token,
        "store_department_id": store_department_id,
        "user_category_name": user_category_name,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "birth_date": birth_date,
        "sex": sex,
    }


@router.get("/add")
async def add(params: Annotated[dict, Depends(add_user_parameters)]):
    if (
            not params["user_phone"]
            and not params["email"]
            and not params["origin_user_id"]
    ):
        return {
            "status": "error",
            "message": "Provide user_phone or email or origin_user_id",
        }

    if not params["token"]:
        return {
            "status": "error",
            "message": "Provide token",
        }

    if not params["store_department_id"]:
        return {
            "status": "error",
            "message": "Provide store_department_id",
        }

    query = []

    if params["user_phone"]:
        query.append({"user_phone": params["user_phone"]})

    if params["email"]:
        query.append({"email": params["email"]})

    if params["origin_user_id"]:
        query.append({"origin_user_id": params["origin_user_id"]})

    pipeline = [
        {
            "$match": {
                "$and": [
                    {"$or": query},
                    {"store_department_id": params["store_department_id"]},
                ]
            },
        }
    ]

    users = User.aggregate(pipeline)
    if len(list(users)) != 0:
        return {
            "status": "error",
            "message": "User is already registered.User is already client.",
        }

    result = User.insert_one(params)

    return user_envelope(User.find_one({"_id": result.inserted_id}))
