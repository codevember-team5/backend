"""User service module."""

from src.user.domain import model
from src.user.repository import AbstractUserRepository


class UserService:
    """User service."""

    def __init__(self, repository: AbstractUserRepository):
        """User service init."""
        self.repository = repository

    async def get_user(self, user_id: str) -> model.User | None:
        """Get a User by id."""
        return await self.repository.get(user_id)

    async def get_users(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        """Get a list of User.

        Arguments:
            skip (int | None, optional): Number of items to skip for pagination. Defaults to None.
            limit (int | None, optional): Maximum number of items to return for pagination. Defaults to None.
        """
        return await self.repository.get_all(skip=skip, limit=limit)

    async def create_user(self, fullname: str) -> model.User:
        """Create a new User.

        Arguments:
            fullname (str): Full name of the user.
        """
        return await self.repository.add(fullname)

    async def delete_user(self, user_id: str) -> None:
        """Delete a User by id.

        Arguments:
            user_id (str): Unique identifier of the user.
        """
        return await self.repository.delete(user_id)

    async def assign_device_to_user(self, user_id: str, device_id: str) -> None:
        """Assign a device to a User.

        Arguments:
            user_id (str): Unique identifier of the user.
            device_id (str): Unique identifier of the device.
        """
        return await self.repository.assign_device_to_user(user_id, device_id)
