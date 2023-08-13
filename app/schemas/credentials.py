from datetime import datetime
from typing import List

from app.schemas.base_schema import BaseSchema
from app.schemas.token import TokenBaseSchema


class CredentialsBaseSchema(BaseSchema):
    store_department_key: str
    store_department_id: str
    pin_codes: List[int | str] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tokens: List[TokenBaseSchema] = []


class CredentialsCreateSchema(CredentialsBaseSchema):
    pass


class CredentialsUpdateSchema(BaseSchema):
    store_department_key: str
    store_department_id: str
    pin_codes: List[int | str]


class CredentialsResponseSchema(CredentialsBaseSchema):
    id: str
