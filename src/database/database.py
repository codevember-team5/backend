from beanie import Document, init_beanie
from fastapi import FastAPI, Request
from pydantic import Field
from pymongo import AsyncMongoClient

from src.settings import settings

def get_db(request: Request):
    return request.app.state.db

def get_db_connection():
    """Get database connection."""
    return AsyncMongoClient(host=settings.db.uri)

async def init_db(app: FastAPI):
    client = get_db_connection()
    db = client[settings.db.dbname]
    await init_beanie(database=db, document_models=[UserDoc, DeviceDoc])
    app.state.db = db
    app.state.mongo_client = client

class UserDoc(Document):
    user_id: str | None = Field(None, description="User identifier")
    fullname: str = Field(..., description="User full name")

    class Settings:
        name = "users"

class DeviceDoc(Document):
    device_id: str = Field(..., description="Unique identifier for the device")
    user_id: str | None = Field(None, description="User identifier associated with the device")

    class Settings:
        name = "devices"
