"""Settings for the MCP server application."""

from pydantic import Field

from src.common.shared import CommonSettings


class MCPSettings(CommonSettings):
    """Settings for the MCP server application."""

    backend_base_url: str = Field("http://localhost:8000", validation_alias="MCP_BACKEND_BASE_URL")


settings = MCPSettings()
