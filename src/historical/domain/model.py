"""Activity Logs models."""

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class ActivityLogs(BaseModel):
    """Activity Logs model."""

    device_id: str = Field(..., description="Device unique identifier")
    start_time: datetime = Field(..., description="Start time of the activity log")
    stop_time: datetime | None = Field(None, description="End time of the activity log")
    process: str = Field(..., description="Process name associated with the activity log")
    window_title: str = Field(..., description="Window title associated with the activity log")
