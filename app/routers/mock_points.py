from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from pymongo import ReturnDocument

from app.database import User
from app.routers.user_helpers import user_creds_parameters, token_parameters, get_user
from app.schemas.history_record import HistoryRecord
from app.serializers.mock_points_serializers import points_add_envelope

router = APIRouter()


@router.get("/add")
async def points_add(
    user_creds: Annotated[dict, Depends(user_creds_parameters)],
    auth: Annotated[dict, Depends(token_parameters)],
    points: Annotated[int, Query(ge=0)] = 0,
    comment: Annotated[str, Query()] = "",
    order_num: Annotated[str, Query()] = "",
):
    error, result = get_user(user_creds, auth)
    if error:
        return result
    user = result

    history_record = HistoryRecord(
        action="extra",
        action_date=datetime.utcnow(),
        is_completed=True,
        points_delta=points,
        name=comment,
        order_num=order_num,
    )

    user = dict(
        User.find_one_and_update(
            {"_id": user["_id"]},
            {
                "$inc": {
                    "points.confirmed": points,
                    "points.total": points,
                },
                "$push": {"history": history_record.model_dump()},
            },
            return_document=ReturnDocument.AFTER,
        )
    )

    result = {}
    result.update(user)
    result["receipt_date"] = history_record.action_date

    return points_add_envelope(result)
