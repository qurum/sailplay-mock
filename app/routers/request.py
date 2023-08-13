from typing import Annotated

from fastapi import APIRouter, Query

from app.database import ApiRequest
from app.serializers.api_request_serializers import api_request_list_envelope

router = APIRouter()


@router.get("/")
async def index(
    route: Annotated[str, Query()] = "/",
    count: Annotated[int | None, Query(ge=1, le=50)] = 10,
):
    api_requests = ApiRequest.find({"route": route}).sort("created_at", -1).limit(count)
    return api_request_list_envelope(api_requests)
