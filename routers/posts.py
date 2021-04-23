from fastapi import APIRouter, HTTPException, status, Request, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
import datetime

from uuid import UUID

from models.Auth import AuthHandler
from models.Users import User, UpdateUser
from Posts import Post
from users import oauth_scheme


router = APIRouter(tags=['Posts'])
auth_handler = AuthHandler()


@router.get('/posts/{user_id}')
async def get_posts(request: Request, username: UUID):
    for i, post in enumerate(
        posts := await request.app.mongodb['posts'].find({"_id": user_id}).to_list()
    ):


@router.post('/posts')
async def make_post(request: Request, post: Post, token=Depends(oauth_scheme)):
    pass