from datetime import datetime

from app.schemas.base_schema import BaseSchema


class HistoryRecord(BaseSchema):
    action: str
    action_date: datetime
    is_completed: bool
    points_delta: int
    name: str
    order_num: str
