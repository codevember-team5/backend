"""Health schemas for REST API."""

from pydantic import BaseModel


class GetHealthResponse(BaseModel):
    """Get health response schema."""

    status: str
    uptime: str
