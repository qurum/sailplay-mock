from datetime import datetime

from app.schemas.base_schema import BaseSchema


class TokenBaseSchema(BaseSchema):
    value: str
    pin_code: int | str
    created_at: datetime
