import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

from app.database import Credentials
from app.schemas.token import TokenBaseSchema
from app.serializers.mock_login import login_ok_envelope

router = APIRouter()


@router.get("/")
async def login(
    store_department_key: Annotated[int | str | None, Query()] = None,
    store_department_id: Annotated[int | str | None, Query()] = None,
    pin_code: Annotated[int | str | None, Query()] = None,
):
    if not store_department_id or not store_department_id or not pin_code:
        return {
            "status": "error",
            "message": "Provide store_department_key, store_department_id and pin_code",
        }

    credentials = Credentials.find_one(
        {
            "store_department_key": store_department_key,
            "store_department_id": store_department_id,
        }
    )

    login_error = {
        "status": "error",
        "message": "Data not found with provided store_department_key, store_department_id and pin_code",
    }

    if not credentials:
        return login_error

    if str(pin_code) not in [str(p) for p in credentials["pin_codes"]]:
        return login_error

    token = TokenBaseSchema(
        value=str(uuid.uuid4()), created_at=datetime.utcnow(), pin_code=pin_code
    )

    Credentials.find_one_and_update(
        {"_id": credentials["_id"]}, {"$push": {"tokens": token.model_dump()}}
    )

    login_ok = {
        "status": "ok",
        "token": token.value,
        "pin_codes": credentials["pin_codes"],
    }

    return login_ok_envelope(login_ok)
