"""Historical schemas for REST API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo

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

    @field_validator("end_time")
    @classmethod
    def validate_range(cls, v: datetime, values: FieldValidationInfo) -> datetime:
        """Validate that end_time is greater than start_time."""
        start = values.data.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be greater than start_time")
        return v
