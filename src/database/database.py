"""Database connection and models using Beanie ODM."""

from beanie import Document
from beanie import PydanticObjectId
from beanie import init_beanie
from fastapi import FastAPI
from pydantic import Field
from pymongo import AsyncMongoClient

from src.settings import settings


def get_db_connection() -> AsyncMongoClient:
    """Get database connection."""
    return AsyncMongoClient(host=settings.db.uri)


async def init_db(app: FastAPI):
    """Initialize the database connection and Beanie ODM."""
    client = get_db_connection()
    db = client[settings.db.dbname]
    await init_beanie(database=db, document_models=[UserDoc, DeviceDoc])
    app.state.mongo_client = client


class UserDoc(Document):
    """User document model."""

    user_id: PydanticObjectId = Field(..., description="User identifier", validation_alias="_id")
    fullname: str = Field(..., description="User full name")

    class Settings:
        """Settings for UserDoc."""

        name = "users"


class DeviceDoc(Document):
    """Device document model."""

    device_id: str = Field(..., description="Unique identifier for the device")
    user_id: PydanticObjectId | None = Field(None, description="User identifier associated with the device")

    class Settings:
        """Settings for DeviceDoc."""

        name = "devices"
