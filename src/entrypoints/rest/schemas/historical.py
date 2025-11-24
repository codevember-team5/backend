"""Historical schemas for REST API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from src.historical.domain import model


class GetActivitiesLogsResponse(BaseModel):
    """Get activity logs response schema."""

    activities_logs: list[model.ActivityLogs]


class ActivitySummaryQuery(BaseModel):
    """Activity summary query schema."""

    device_id: str
    start_time: datetime
    end_time: datetime
    group_by: Literal["day"] | None = None
