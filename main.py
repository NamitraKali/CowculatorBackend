from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from routers.users import router as user_router
#from routers.auth import router as auth_router

from config import settings

app = FastAPI()

# Connect to MongoDB Atlas
@app.on_event("startup")
async def startup_motor_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


# Close MongoDB Atlas connection
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get('/')
def index():
    return {'data': "Hello World"}

app.include_router(user_router)