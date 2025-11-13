"""User and Device models."""

from pydantic import BaseModel
from pydantic import Field


class User(BaseModel):
    """User model."""

    fullname: str = Field()
    devices: list[str] = Field(default_factory=list)


class Device(BaseModel):
    """Device model."""

    device_id: str = Field()
    user_id: str | None = Field(default=None)
