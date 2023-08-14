from datetime import datetime

from typing import Dict, List

from app.schemas.base_schema import BaseSchema
from app.schemas.gift import Gift
from app.schemas.history_record import HistoryRecord


class User(BaseSchema):
    user_phone: str | None
    email: str | None
    origin_user_id: str | None
    token: str | None
    store_department_id: str | None
    user_category_name: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    birth_date: str | None
    sex: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    points: Dict[str, int] | None = None
    available_gifts: List[Gift] | None = None
    over_user_points_gifts: List[Gift] | None = None
    history: List[HistoryRecord] | None = None
