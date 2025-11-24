"""MCP Server Module."""

import httpx

from fastmcp import FastMCP

from src.mcp_server.settings import settings

mcp = FastMCP("backend-team5-mcp-server")

ACTIVITY_LOGS_PATH_BY_DEVICE = "/api/historical/device/{device_id}/activities-logs"
ACTIVITY_LOGS_PATH_BY_USER = "/api/historical/user/{user_id}/activities-logs"
USERS_PATH = "/api/user"


@mcp.tool()
async def get_users(
    skip: int | None = None,
    limit: int | None = None,
) -> dict:
    """Get Users (calls the backend REST API).

    Args:
        skip: offset
        limit: number of results
    """
    params: dict[str, object] = {}

    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            USERS_PATH,
            params=params or None,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_historical_activities_logs_by_device_id(
    device_id: str,
    skip: int | None = None,
    limit: int | None = None,
    start_time: str | None = None,
    stop_time: str | None = None,
) -> dict:
    """Get Historical Activities Logs by device.

    Args:
        device_id: Device ID
        skip: offset
        limit: number of results
        start_time: start time filter
        stop_time: stop time filter
    """
    params: dict[str, object] = {}

    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    if start_time is not None:
        params["start_time"] = start_time
    if stop_time is not None:
        params["stop_time"] = stop_time

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            ACTIVITY_LOGS_PATH_BY_DEVICE.format(device_id=device_id),
            params=params or None,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_historical_activities_logs_by_user_id(
    user_id: str,
    skip: int | None = None,
    limit: int | None = None,
    start_time: str | None = None,
    stop_time: str | None = None,
) -> dict:
    """Get Historical Activities Logs by user.

    Args:
        user_id: User ID
        skip: offset
        limit: number of results
        start_time: start time filter
        stop_time: stop time filter
    """
    params: dict[str, object] = {}

    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    if start_time is not None:
        params["start_time"] = start_time
    if stop_time is not None:
        params["stop_time"] = stop_time

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            ACTIVITY_LOGS_PATH_BY_USER.format(user_id=user_id),
            params=params or None,
        )
        resp.raise_for_status()
        return resp.json()
