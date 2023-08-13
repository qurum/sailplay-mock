from datetime import datetime
from typing import Dict

from app.schemas.base_schema import BaseSchema


class ApiRequestBaseSchema(BaseSchema):
    method: str
    route: str
    headers: Dict[str, str]
    body: str | None = None
    host: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
