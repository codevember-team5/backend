from pydantic import BaseModel, Field


class User(BaseModel):
    fullname: str = Field()
    devices: list[str] = Field(default_factory=list)

class Device(BaseModel):
    device_id: str = Field()
    user_id: str | None = Field(default=None)