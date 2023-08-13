from typing import List
from pydantic import BaseModel


class LoginOkResponse(BaseModel):
    status: str
    token: str
    pin_codes: List[str | int]


class LoginErrorResponse(BaseModel):
    status: str
    message: str
