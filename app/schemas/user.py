from datetime import datetime

from app.schemas.base_schema import BaseSchema


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
