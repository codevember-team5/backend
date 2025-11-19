"""Database connection and models using Beanie ODM."""

from datetime import datetime

from beanie import Document
from beanie import PydanticObjectId
from beanie import init_beanie
from pydantic import Field
from pymongo import AsyncMongoClient

from src.settings import settings


def get_db_connection() -> AsyncMongoClient:
    """Get database connection."""
    return AsyncMongoClient(host=settings.db.uri)


async def init_db(client: AsyncMongoClient):
    """Initialize the database connection and Beanie ODM."""
    db = client[settings.db.dbname]
    await init_beanie(database=db, document_models=[UserDoc, DeviceDoc, ActivityLogsDoc])


class UserDoc(Document):
    """User document model."""

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


class ActivityLogsDoc(Document):
    """Activity Logs document model."""

    device_id: str = Field(..., description="Device unique identifier")
    start_time: datetime = Field(..., description="Start time of the activity log")
    stop_time: datetime | None = Field(None, description="End time of the activity log")
    process: str = Field(..., description="Process name associated with the activity log")
    window_title: str = Field(..., description="Window title associated with the activity log")

    class Settings:
        """Settings for UserDoc."""

        name = "activity_logs"
