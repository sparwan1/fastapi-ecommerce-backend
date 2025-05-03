from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetCoreSchemaHandler):
        # This tells Pydantic to treat this as a string in OpenAPI/JSON schema
        return {"type": "string"}

class BaseDBModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True 