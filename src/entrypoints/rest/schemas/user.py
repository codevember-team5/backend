"""User schemas for REST API."""

from pydantic import BaseModel

from src.user.domain import model


class GetUsersResponse(BaseModel):
    """Get users response schema."""

    users: list[model.User]


class GetUserResponse(BaseModel):
    """Get user response schema."""

    user: model.User


class CreateUserRequest(BaseModel):
    """Create user request schema."""

    fullname: str


class CreateUserResponse(BaseModel):
    """Create user response schema."""

    user: model.User
