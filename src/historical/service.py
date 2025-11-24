"""Historical Service Module."""

from datetime import datetime

from src.historical.aggregator import ActivityAggregator
from src.historical.domain import model
from src.historical.domain.model import ActivitySummaryResult
from src.historical.repository import AbstractHistoricalRepository
from src.historical.repository import normalize_end
from src.historical.repository import normalize_start
from src.settings import get_logger

logger = get_logger()


class HistoricalService:
    """Historical service."""

    def __init__(self, repository: AbstractHistoricalRepository, aggregator: ActivityAggregator | None = None):
        """Historical service init."""
        self.repository = repository
        self.aggregator = aggregator or ActivityAggregator()

    async def get_activities_log_by_device(
        self,
        device_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
    ) -> list[model.ActivityLogs]:
        """Get a list of Activity Logs.

        Args:
            device_id (str): Device ID
            skip (int | None, optional): Number of items to skip for pagination. Defaults to None.
            limit (int | None, optional): Maximum number of items to return for pagination. Defaults to None.
            start_time (datetime, optional): Filter logs with start_time greater than or equal to this value.
            stop_time (datetime, optional): Filter logs with stop_time less than or equal to this value.
        """
        return await self.repository.get_all_by_device(
            device_id=device_id,
            skip=skip,
            limit=limit,
            start_time=start_time,
            stop_time=stop_time,
        )

    async def get_activities_log_by_user(
        self,
        user_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
    ) -> list[model.ActivityLogs]:
        """Get a list of Activity Logs.

        Args:
            user_id (str): User ID
            skip (int | None, optional): Number of items to skip for pagination. Defaults to None.
            limit (int | None, optional): Maximum number of items to return for pagination. Defaults to None.
            start_time (datetime, optional): Filter logs with start_time greater than or equal to this value.
            stop_time (datetime, optional): Filter logs with stop_time less than or equal to this value.
        """
        return await self.repository.get_all_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            start_time=start_time,
            stop_time=stop_time,
        )

    async def get_activity_summary_by_device(
        self,
        device_id: str,
        start_time: datetime,
        stop_time: datetime,
        group_by: str | None = None,
        page_size: int = 500,
    ) -> ActivitySummaryResult:
        """Fetch all logs in [start_time, stop_time], classify and aggregate for a device.

        Uses pagination over the underlying repository.
        """
        # normalize time as you already do
        normalized_start = normalize_start(start_time)
        normalized_stop = normalize_end(stop_time)

        logs: list[model.ActivityLogs] = []
        skip = 0

        while True:
            batch = await self.repository.get_all_by_device(
                device_id=device_id,
                skip=skip,
                limit=page_size,
                start_time=normalized_start,
                stop_time=normalized_stop,
            )
            if not batch:
                break
            logs.extend(batch)
            if len(batch) < page_size:
                break
            skip += page_size

        return self.aggregator.classify_and_aggregate(
            device_id=device_id,
            logs=logs,
            start_time=normalized_start,
            stop_time=normalized_stop,
            group_by_day=(group_by == "day"),
        )

    async def get_activity_summary_by_user(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
        group_by: str | None = None,
        page_size: int = 500,
    ) -> ActivitySummaryResult:
        """Fetch all logs in [start_time, stop_time], classify and aggregate for a user.

        Uses pagination over the underlying repository.
        """
        # normalize time as you already do
        normalized_start = normalize_start(start_time)
        normalized_stop = normalize_end(stop_time)

        logs: list[model.ActivityLogs] = []
        skip = 0

        while True:
            batch = await self.repository.get_all_by_user(
                user_id=user_id,
                skip=skip,
                limit=page_size,
                start_time=normalized_start,
                stop_time=normalized_stop,
            )
            if not batch:
                break
            logs.extend(batch)
            if len(batch) < page_size:
                break
            skip += page_size

        return self.aggregator.classify_and_aggregate(
            device_id=user_id,
            logs=logs,
            start_time=normalized_start,
            stop_time=normalized_stop,
            group_by_day=(group_by == "day"),
        )
