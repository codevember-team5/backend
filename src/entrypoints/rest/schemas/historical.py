"""Historical schemas for REST API."""

from pydantic import BaseModel

from src.historical.domain import model


class GetActivitiesLogsResponse(BaseModel):
    """Get activity logs response schema."""

    activities_logs: list[model.ActivityLogs]
