"""Common module."""

import datetime

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class CommonSettings(BaseSettings):
    """Common settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


def as_aware_utc(dt: datetime.datetime | None) -> datetime.datetime | None:
    """Convert a datetime to an aware UTC datetime."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.UTC)
    return dt.astimezone(datetime.UTC)


def normalize_start(start_time: datetime.datetime) -> datetime.datetime:
    """Normalize the start time to the start of the day if no time is specified."""
    # User DID NOT specify a time -> set to start of day
    if start_time.hour == 0 and start_time.minute == 0 and start_time.second == 0 and start_time.microsecond == 0:
        return datetime.datetime.combine(start_time.date(), datetime.time.min, tzinfo=datetime.UTC)

    # User specified hh:mm:ss -> keep as is
    return start_time.astimezone(tz=datetime.UTC)


def normalize_end(stop_time: datetime.datetime) -> datetime.datetime:
    """Normalize the end time to the end of the day if no time is specified."""
    # User DID NOT specify a time -> set to end of day
    if stop_time.hour == 0 and stop_time.minute == 0 and stop_time.second == 0 and stop_time.microsecond == 0:
        return datetime.datetime.combine(stop_time.date(), datetime.time.max, tzinfo=datetime.UTC)

    # User specified hh:mm:ss -> keep as is
    return stop_time.astimezone(tz=datetime.UTC)
