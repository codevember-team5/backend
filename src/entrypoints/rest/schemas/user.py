"""User schemas for REST API."""

from pydantic import BaseModel

from src.user.domain import model


class GetUsersResponse(BaseModel):
    """Get users response schema."""

    users: list[model.User]
