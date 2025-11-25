"""Mapper functions for User domain model."""

from src.common.shared import as_aware_utc
from src.database import database
from src.historical.domain import model


def activitylogs_to_domain(activity_logs: database.ActivityLogsDoc) -> model.ActivityLogs:
    """Map ActivityLogsDoc to ActivityLogs domain model."""
    return model.ActivityLogs(
        device_id=activity_logs.device_id,
        start_time=as_aware_utc(activity_logs.start_time),
        stop_time=as_aware_utc(activity_logs.stop_time),
        process=activity_logs.process,
        window_title=activity_logs.window_title,
    )
