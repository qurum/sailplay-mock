from app.schemas.base_schema import BaseSchema


class HistoryRecord(BaseSchema):
    action: str
    action_date: str
    is_completed: bool
    points_delta: int
    name: str
