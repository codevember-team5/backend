from src.user import model
from src.user.repository import AbstractUserRepository


class UserService:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def get_user(self, id: str) -> model.User | None:
        return await self.repository.get(id)

    async def get_users(self, skip: int | None = None, limit: int | None = None) -> list[model.User]:
        return await self.repository.get_all(skip=skip, limit=limit)