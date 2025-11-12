from pydantic import BaseModel

from src.user import model


class GetUsersResponse(BaseModel):
    """Get users response schema."""

    users: list[model.User]