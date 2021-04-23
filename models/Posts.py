from pydantic import BaseModel, Field
from typing import Optional
import datetime
from uuid import UUID


class Post(BaseModel):
    post_id: UUID = Field(alias='_id')
    user_id: UUID
    img: str
    description: str
    food: str
    carbon: float