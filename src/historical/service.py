"""Historical Service Module."""

from datetime import datetime

from src.historical.domain import model
from src.historical.repository import AbstractHistoricalRepository
from src.settings import get_logger

logger = get_logger()


class HistoricalService:
    """Historical service."""

    def __init__(self, repository: AbstractHistoricalRepository):
        """Historical service init."""
        self.repository = repository

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
