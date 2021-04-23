from pydantic import BaseModel, Field
from typing import Optional
import datetime
from uuid import UUID


class User(BaseModel):
    id: UUID = Field(alias="_id")
    dateCreated: datetime.datetime
    fullName: str
    email: str
    username: str
    password: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": '3fe1dcc1-d753-4acf-9ac5-206a3cb63db5',
                "dateCreated": '2021-04-08 21:59:15.288488',
                "fullName": 'John Doe',
                "email": 'user@domain.com',
                "username": "myUser",
                "password": "password"
            }
        }


class UpdateUser(BaseModel):
    fullName: Optional[str]
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                "fullName": 'John Doe',
                "email": 'user@domain.com',
                "username": "myUser",
                "password": "password"
            }
        }