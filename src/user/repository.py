"""User repository."""

import abc

from collections import defaultdict

from beanie import PydanticObjectId
from bson.errors import InvalidId
from pydantic import ValidationError

from src.common.exceptions import InvalidArgumentError
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

    async def get_user_from_device_id(self, device_id: str) -> model.User | None:
        """Get User object by device id.

        Args:
            device_id (str): Device unique identifier

        Returns:
            model.User | None: User model instance or None
        """
        return await self._get_user_from_device_id(device_id)

    async def get_all(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        """Get a list of all User objects.

        Args:
            skip (int | None, optional): Skip the number of items specified (for pagination). Defaults to None.
            limit (int | None, optional): Limit the returned items (for pagination). Defaults to None.

        Returns:
            list[model.User]: list of User model instances
        """
        return await self._get_all(skip, limit)

    async def add(self, fullname: str) -> model.User:
        """Add a new User.

        Args:
            fullname (str): Full name of the user.

        Returns:
            model.User: Created User model instance
        """
        return await self._add(fullname)

    async def delete(self, user_id: str) -> None:
        """Delete a User by id.

        Args:
            user_id (str): User unique identifier
        """
        return await self._delete(user_id)

    async def assign_device_to_user(self, user_id: str, device_id: str) -> None:
        """Assign a device to a User.

        Args:
            user_id (str): User unique identifier
            device_id (str): Device unique identifier
        """
        return await self._assign_device_to_user(user_id, device_id)

    @abc.abstractmethod
    async def _get(self, uuid: str) -> model.User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_all(self, skip: int | None, limit: int | None) -> list[model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _add(self, fullname: str) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, user_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _assign_device_to_user(self, user_id: str, device_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_user_from_device_id(self, device_id: str):
        raise NotImplementedError


class BeanieUserRepository(AbstractUserRepository):
    """Concrete repository for Beanie managed database."""

    async def _get(self, user_id: str) -> model.User | None:
        try:
            user_id = PydanticObjectId(user_id)
        except InvalidId:
            raise InvalidArgumentError("Invalid user id format")

        user = await database.UserDoc.get(user_id)
        devices = await DeviceDoc.find(DeviceDoc.user_id == user_id).to_list()

        return userdoc_to_domain(user, devices) if user else None

    async def _get_all(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        users = await database.UserDoc.find_all().skip(skip).limit(limit).to_list()
        devices = await database.DeviceDoc.find_all().to_list()

        devices_by_user: dict[str, list[DeviceDoc]] = defaultdict(list)
        for device in devices:
            if device.user_id:
                devices_by_user[device.user_id].append(device)

        return [userdoc_to_domain(user, devices_by_user.get(user.id, [])) for user in users]

    async def _add(self, fullname: str) -> model.User:
        user = database.UserDoc(fullname=fullname)
        await user.insert()
        devices = await database.DeviceDoc.find(database.DeviceDoc.user_id == user.id).to_list()
        return userdoc_to_domain(user, devices)

    async def _delete(self, user_id: str) -> None:
        try:
            user = await database.UserDoc.get(user_id)
        except (ValidationError, ValueError):
            raise InvalidArgumentError("Invalid user id format")

        if user:
            await user.delete()

    async def _assign_device_to_user(self, user_id: str, device_id: str):
        try:
            user_id = PydanticObjectId(user_id)
        except InvalidId:
            raise InvalidArgumentError("Invalid user id format")

        device = await database.DeviceDoc.find_one(database.DeviceDoc.device_id == device_id)

        if device:
            device.user_id = user_id
            await device.save()

    async def _get_user_from_device_id(self, device_id: str) -> model.User | None:
        device = await database.DeviceDoc.find_one(database.DeviceDoc.device_id == device_id)

        if device and device.user_id:
            return await self.get(user_id=str(device.user_id))

        return None
