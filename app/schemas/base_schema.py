from bson import ObjectId
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
