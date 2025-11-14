"""Shared REST schemas."""

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    """Error response schema."""

    details: str
