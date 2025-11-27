"""Activity Logs models."""

from datetime import date
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic import Field


class GroupByQuery(str, Enum):
    """Group by query enum."""

    HOURLY = "hourly"
    DAY = "day"


class ActivityLogs(BaseModel):
    """Activity Logs model."""

    device_id: str = Field(..., description="Device unique identifier")
    start_time: datetime = Field(..., description="Start time of the activity log")
    stop_time: datetime | None = Field(None, description="End time of the activity log")
    process: str = Field(..., description="Process name associated with the activity log")
    window_title: str = Field(..., description="Window title associated with the activity log")


class ActivityLogsAttentionLevel(ActivityLogs):
    """Activity Logs model with attention level."""

    level: int = Field(..., description="Attention level associated with the activity log")
    total_seconds: float = Field(..., description="Total seconds for the activity log")
    total_seconds_productive: float = Field(
        ...,
        description="Total seconds for the activity log based on productive time",
    )


class ActivityCategory(str, Enum):
    """Predefined activity categories."""

    CODING = "CODING"
    DB_TECH = "DB_TECH"
    DEVOPS_GIT = "DEVOPS_GIT"
    MEETINGS_CALLS = "MEETINGS_CALLS"
    DOC_RESEARCH_WORK_WEB = "DOC_RESEARCH_WORK_WEB"
    SOCIAL_ENTERTAINMENT = "SOCIAL_ENTERTAINMENT"
    BREAK_IDLE = "BREAK_IDLE"
    OTHER_WEB = "OTHER_WEB"
    MISC = "MISC"


class ClassifiedActivity(BaseModel):
    """Activity log plus derived category and duration in seconds."""

    device_id: str
    start_time: datetime
    stop_time: datetime
    process: str
    window_title: str
    category: ActivityCategory
    duration_seconds: float


class ActivityCategoryComponentSummary(BaseModel):
    """Breakdown item inside a category.

    Represents how much time within a given category comes from a specific
    (process, window bucket) pair.

    For browsers, the window bucket can be the domain (e.g., `youtube.com`),
    while for native apps it is usually the raw window title or a normalized
    label.
    """

    process: str
    window_bucket: str
    total_seconds: float
    percentage_of_category: float
    entries_count: int


class ActivityCategorySummary(BaseModel):
    """Activity category summary model."""

    category: ActivityCategory
    total_seconds: float
    percentage: float
    entries_count: int
    components: list[ActivityCategoryComponentSummary] = Field(default_factory=list)


class DailyActivitySummary(BaseModel):
    """Daily activity summary model."""

    day: date
    total_seconds: float
    categories: list[ActivityCategorySummary] = Field(default_factory=list)


class ActivitySummaryResult(BaseModel):
    """Activity summary result model."""

    start_time: datetime
    stop_time: datetime
    group_by: list[GroupByQuery]
    total_seconds: float
    categories: list[ActivityCategorySummary] = Field(
        default_factory=list,
        description="Global summary per category when group_by is null.",
    )
    days: list[DailyActivitySummary] = Field(
        default_factory=list,
        description="Daily breakdown when group_by == 'day'.",
    )


class ProcessWindowLevel(BaseModel):
    """Process Window Level model."""

    process: str
    window_title: str
    level: int


class DailyAttentionLevelSummary(BaseModel):
    """Daily attention level summary model."""

    day: date
    percentage: float


class HourlyAttentionLevelSummary(BaseModel):
    """Hourly attention level summary model."""

    hour: datetime
    percentage: float


class AttentionLevelSummaryResult(BaseModel):
    """Attention Level summary result model."""

    start_time: datetime
    stop_time: datetime
    group_by: list[GroupByQuery]
    days: list[DailyAttentionLevelSummary] = Field(
        default_factory=list,
        description="Daily breakdown when group_by == 'day'.",
    )
    hours: list[HourlyAttentionLevelSummary] = Field(
        default_factory=list,
        description="Hourly breakdown when group_by == 'hourly'.",
    )
