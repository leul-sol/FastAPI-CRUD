from typing import List, Optional, Annotated, Any
from pydantic import BaseModel, Field, ConfigDict, GetJsonSchemaHandler
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator: Any, _field_schema: dict[str, Any]) -> None:
        _field_schema.update(type="string")

class Comment(BaseModel):
    username: str
    text: str
    date: str
    likes: str

    model_config = ConfigDict(json_encoders={ObjectId: str})

class TikTokPost(BaseModel):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    title: str
    video_url: str
    like: str
    comment: str
    share: str
    date: str
    username: str
    comments: List[Comment]
    hashtags: List[str]

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    ) 