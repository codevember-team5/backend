from pydantic import BaseModel

class User(BaseModel):
    """User schema."""

    fullname: str
    devices: list[str]

class GetUsersResponse(BaseModel):
    """Get users response schema."""

    users: list[User]