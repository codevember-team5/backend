"""Historical Service Module."""

from collections import defaultdict
from datetime import date
from datetime import datetime

from src.historical.aggregator import ActivityAggregator
from src.historical.domain import model
from src.historical.domain.model import ActivitySummaryResult
from src.historical.domain.model import AttentionLevelSummaryResult
from src.historical.domain.model import DailyAttentionLevelSummary
from src.historical.domain.model import GroupByQuery
from src.historical.domain.model import HourAttentionLevelSummary
from src.historical.domain.model import ProcessWindowLevel
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

    async def _get_logs_by_user_paginated(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
        page_size: int,
    ) -> list[model.ActivityLogs]:
        """Fetch all logs for a user in a time range using pagination."""
        logs: list[model.ActivityLogs] = []
        skip = 0

        while True:
            batch = await self.repository.get_all_by_user(
                user_id=user_id,
                skip=skip,
                limit=page_size,
                start_time=start_time,
                stop_time=stop_time,
            )
            if not batch:
                break

            logs.extend(batch)

            if len(batch) < page_size:
                break

            skip += page_size

        return logs

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
        group_by: list[GroupByQuery],
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
            group_by=group_by,
        )

    async def get_activity_summary_by_user(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
        group_by: list[GroupByQuery],
        page_size: int = 500,
    ) -> ActivitySummaryResult:
        """Fetch all logs in [start_time, stop_time], classify and aggregate for a user.

        Uses pagination over the underlying repository.
        """
        # normalize time as you already do
        normalized_start = normalize_start(start_time)
        normalized_stop = normalize_end(stop_time)
        logs: list[model.ActivityLogs] = await self._get_logs_by_user_paginated(
            user_id,
            normalized_start,
            normalized_stop,
            page_size,
        )

        return self.aggregator.classify_and_aggregate(
            device_id=user_id,
            logs=logs,
            start_time=normalized_start,
            stop_time=normalized_stop,
            group_by=group_by,
        )

    async def get_attention_level_summary_by_user(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
        group_by: list[GroupByQuery],
        page_size: int = 500,
    ) -> AttentionLevelSummaryResult:
        """Get attention level summary by user."""
        # normalize time as you already do
        normalized_start = normalize_start(start_time)
        normalized_stop = normalize_end(stop_time)
        logs: list[model.ActivityLogs] = await self._get_logs_by_user_paginated(
            user_id,
            normalized_start,
            normalized_stop,
            page_size,
        )
        process_window = await self.repository.get_process_window_by_user_id(user_id)

        days_summary: list[DailyAttentionLevelSummary] = []
        if GroupByQuery.DAY in group_by:
            days_summary = self._build_daily_summary(logs, process_window)

        hours_summary: list[HourAttentionLevelSummary] = []
        if GroupByQuery.HOUR in group_by:
            hours_summary = self._build_hourly_summary(logs, process_window)

        return AttentionLevelSummaryResult(
            start_time=start_time,
            stop_time=stop_time,
            group_by=group_by,
            days=days_summary,
            hours=hours_summary,
        )

    def _build_daily_summary(
        self,
        logs: list[model.ActivityLogs],
        process_window: dict[str, list[ProcessWindowLevel]],
    ) -> list[DailyAttentionLevelSummary]:
        """Build daily attention level summary."""
        by_day: dict[date, list[model.ActivityLogs]] = defaultdict(list)
        for log in logs:
            by_day[log.start_time.date()].append(log)

        summaries: list[DailyAttentionLevelSummary] = []
        for day, day_logs in sorted(by_day.items(), key=lambda x: x[0]):
            productivity = self._compute_productivity_for_logs(day_logs, process_window)
            summaries.append(
                DailyAttentionLevelSummary(
                    day=day,
                    percentage=round(productivity, 2),
                ),
            )

        return summaries

    def _build_hourly_summary(
        self,
        logs: list[model.ActivityLogs],
        process_window: dict[str, list[ProcessWindowLevel]],
    ) -> list[HourAttentionLevelSummary]:
        """Build hourly attention level summary."""
        by_hour: dict[datetime, list[model.ActivityLogs]] = defaultdict(list)
        for log in logs:
            hour_start = log.start_time.replace(minute=0, second=0, microsecond=0)
            by_hour[hour_start].append(log)

        summaries: list[HourAttentionLevelSummary] = []
        for hour_start, hour_logs in sorted(by_hour.items(), key=lambda x: x[0]):
            productivity = self._compute_productivity_for_logs(hour_logs, process_window)
            summaries.append(
                HourAttentionLevelSummary(
                    hour=hour_start,
                    percentage=round(productivity, 2),
                ),
            )

        return summaries

    def _compute_productivity_for_logs(
        self,
        logs: list[model.ActivityLogs],
        process_window: dict[str, list[ProcessWindowLevel]],
    ) -> float:
        """Compute productivity level (%) for a set of logs."""
        aggregated = self.aggregator.aggregate_attention_levels(
            logs=logs,
            process_window=process_window,
        )

        total_seconds = sum(log.total_seconds for log in aggregated)
        if total_seconds == 0:
            return 0.0

        total_seconds_weighted = sum(log.total_seconds_productive for log in aggregated)
        return (total_seconds_weighted / (total_seconds * 10)) * 100
