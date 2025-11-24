"""Historical Repository Module."""

import abc
import datetime

from datetime import time

from beanie.odm.operators.find.comparison import GTE
from beanie.odm.operators.find.comparison import LTE
from beanie.odm.operators.find.comparison import BaseFindComparisonOperator
from beanie.odm.operators.find.comparison import Eq
from beanie.odm.operators.find.comparison import In

from src.database.database import ActivityLogsDoc
from src.database.database import DeviceDoc
from src.historical.domain import model
from src.historical.domain.mapper import activitylogs_to_domain
from src.settings import get_logger

# logger
logger = get_logger()


def normalize_end(stop_time: datetime.datetime | None) -> datetime.datetime | None:
    """Normalize the end time to the end of the day if no time is specified."""
    if stop_time is None:
        return None

    # User DID NOT specify a time -> set to end of day
    if stop_time.hour == 0 and stop_time.minute == 0 and stop_time.second == 0 and stop_time.microsecond == 0:
        return datetime.datetime.combine(stop_time.date(), time.max, tzinfo=datetime.UTC)

    # User specified hh:mm:ss -> keep as is
    return stop_time


class AbstractHistoricalRepository(abc.ABC):
    """Abstract repository.

    Args:
        abc (abc.ABC): Abstract class
    """

    async def get_all_by_devices(
        self,
        device_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        """Get a list of all Activity Logs objects.

        Args:
            device_id (str): Device ID to filter logs.
            skip (int | None, optional): Skip the number of items specified (for pagination). Defaults to None.
            limit (int | None, optional): Limit the returned items (for pagination). Defaults to None.
            start_time (datetime | None, optional): Filter logs with start_time greater than or equal to this value.
            stop_time (datetime | None, optional): Filter logs with stop_time less than or equal to this value.

        Returns:
            list[model.ActivityLogs]: list of Activity Logs model instances
        """
        return await self._get_all_by_device(device_id, skip, limit, start_time, stop_time)

    async def get_all_by_user(
        self,
        user_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        """Get a list of all Activity Logs objects for a user.

        Args:
            user_id (str): User ID to filter logs.
            skip (int | None, optional): Skip the number of items specified (for pagination). Defaults to None.
            limit (int | None, optional): Limit the returned items (for pagination). Defaults to None.
            start_time (datetime | None, optional): Filter logs with start_time greater than or equal to this value.
            stop_time (datetime | None, optional): Filter logs with stop_time less than or equal to this value.

        Returns:
            list[model.ActivityLogs]: list of Activity Logs model instances
        """
        return await self._get_all_by_user(user_id, skip, limit, start_time, stop_time)

    @abc.abstractmethod
    async def _get_all_by_device(
        self,
        device_id: str,
        skip: int | None,
        limit: int | None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_all_by_user(
        self,
        user_id: str,
        skip: int | None,
        limit: int | None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        raise NotImplementedError


class BeanieHistoricalRepository(AbstractHistoricalRepository):
    """Concrete repository for Beanie managed database."""

    async def _get_all_by_device(
        self,
        device_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        filters: list[BaseFindComparisonOperator] = [Eq(ActivityLogsDoc.device_id, device_id)]

        if start_time:
            filters.append(GTE(ActivityLogsDoc.start_time, start_time))

        if stop_time:
            filters.append(LTE(ActivityLogsDoc.stop_time, normalize_end(stop_time)))

        activities = await ActivityLogsDoc.find(*filters).skip(skip).limit(limit).to_list()

        return [activitylogs_to_domain(activity) for activity in activities]

    async def _get_all_by_user(
        self,
        user_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime.datetime | None = None,
        stop_time: datetime.datetime | None = None,
    ) -> list[model.ActivityLogs]:
        devices = await DeviceDoc.find(DeviceDoc.user_id == user_id).to_list()
        device_ids = [d.device_id for d in devices]

        filters: list[BaseFindComparisonOperator] = [In(ActivityLogsDoc.device_id, device_ids)]
        if start_time:
            filters.append(GTE(ActivityLogsDoc.start_time, start_time))

        if stop_time:
            filters.append(LTE(ActivityLogsDoc.stop_time, normalize_end(stop_time)))

        activities = await ActivityLogsDoc.find(*filters).skip(skip).limit(limit).to_list()

        return [activitylogs_to_domain(activity) for activity in activities]
