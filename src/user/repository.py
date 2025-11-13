"""User repository."""

import abc

from collections import defaultdict

from src.database import database
from src.database.database import DeviceDoc
from src.settings import get_logger
from src.user.domain import model
from src.user.domain.mapper import userdoc_to_domain

# logger
logger = get_logger()


class AbstractUserRepository(abc.ABC):
    """Abstract repository.

    Args:
        abc (abc.ABC): Abstract class
    """

    async def get(self, user_id: str) -> model.User | None:
        """Get User object by id.

        Args:
            user_id (str): User unique identifier

        Returns:
            model.User | None: User model instance or None
        """
        return await self._get(user_id)

    async def get_all(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        """Get a list of all User objects.

        Args:
            skip (int | None, optional): Skip the number of items specified (for pagination). Defaults to None.
            limit (int | None, optional): Limit the returned items (for pagination). Defaults to None.

        Returns:
            list[model.User]: list of User model instances
        """
        return await self._get_all(skip, limit)

    @abc.abstractmethod
    async def _get(self, uuid: str) -> model.User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_all(self, skip: int | None, limit: int | None) -> list[model.User]:
        raise NotImplementedError


class BeanieUserRepository(AbstractUserRepository):
    """Concrete repository for Beanie managed database."""

    async def _get(self, user_id: str) -> model.User | None:
        user = await database.UserDoc.get(user_id)
        devices = await database.DeviceDoc.find(database.DeviceDoc.user_id == user_id).to_list()
        return userdoc_to_domain(user, devices) if user else None

    async def _get_all(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        users = await database.UserDoc.find_all().skip(skip).limit(limit).to_list()
        devices = await database.DeviceDoc.find_all().to_list()

        devices_by_user: dict[str, list[DeviceDoc]] = defaultdict(list)
        for device in devices:
            if device.user_id:
                devices_by_user[device.user_id].append(device)

        return [userdoc_to_domain(user, devices_by_user.get(user.user_id, [])) for user in users]
