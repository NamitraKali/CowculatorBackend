from fastapi import APIRouter, HTTPException, status, Request, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
import datetime

from uuid import UUID

from models.Auth import AuthHandler
from models.Users import User, UpdateUser


router = APIRouter(tags=['Users'])

auth_handler = AuthHandler()
oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

@router.post('/register')
async def create_user(request: Request, user: User = Body(...)):
    user.id = uuid.uuid4() # instantiate a unique UUID
    user.dateCreated = datetime.datetime.now()  # instantiate the current date
    
    # Check if the username already exists
    if (
        existing_user := await request.app.mongodb['users'].find_one({"username":user.username})
    ) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username {user.username} already exists")

    # hash the password
    user.password = auth_handler.get_password_hash(user.password)

    # Add the user to the database
    user = jsonable_encoder(user)
    new_user = await request.app.mongodb['users'].insert_one(user)
    created_user = await request.app.mongodb['users'].find_one(
        {"_id": new_user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.post("/login")
async def login(request: Request, login: OAuth2PasswordRequestForm = Depends()):
    # Query the username from the database
    existing_user = await request.app.mongodb['users'].find_one({"username": login.username})

    # Verify the username and the password
    if (existing_user is None) or (not auth_handler.verify_password(login.password, existing_user['password'])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid username and/or password")
    
    # Send the user object to the frontend without the hashed password
    payload = {
        'user_id': existing_user['_id'],
        'userName': existing_user['username'],
        'fullName': existing_user['fullName'],
        'email': existing_user['email'],
    }

    #Return the JWT token to log user in
    token = {
        'access_token': auth_handler.encode_token(payload),
        'token_type': 'bearer'
    }

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=token)


@router.patch('/users', response_description="Update an existing user")
async def update_user(request: Request, user_info: UpdateUser = Body(...), token=Depends(oauth_scheme)):
    token = auth_handler.decode_token(token)
    new_user = {k: v for k, v in user_info.dict().items() if v is not None}

    if 'password' in new_user.keys():
        new_user['password'] = auth_handler.get_password_hash(new_user['password'])

    if len(new_user) >= 1:
        # update the user's database entry
        update_user = await request.app.mongodb['users'].update_one(
            {"_id": token['user_id']}, {"$set": new_user}
        )

        # Return the updated user entry
        if update_user.modified_count == 1:
            if (
                updated_user := await request.app.mongodb['users'].find_one({"_id":token['user_id']})
            ) is not None:
                del updated_user['password']
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)
    
    if (
        existing_user := await request.app.mongodb['users'].find_one({"_id":token['user_id']})
    ) is not None:
        del existing_user['password']
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=existing_user)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")


@router.delete('/users', response_description="Delete a user")
async def delete_user(request: Request, token=Depends(oauth_scheme)):
    token = auth_handler.decode_token(token)

    delete_result = await request.app.mongodb['users'].delete_one({"_id":token['user_id']})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User ID {token['user_id']} not found")