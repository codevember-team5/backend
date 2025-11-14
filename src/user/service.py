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
