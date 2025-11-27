"""MCP Server Module."""

from enum import Enum
from typing import Literal

import httpx

from fastmcp import FastMCP

from src.historical.domain.model import GroupByQuery
from src.mcp_server.settings import settings

mcp = FastMCP("backend-team5-mcp-server")

ACTIVITY_LOGS_PATH_BY_DEVICE = "/api/historical/device/{device_id}/activities-logs"
ACTIVITY_LOGS_PATH_BY_USER = "/api/historical/user/{user_id}/activities-logs"
ACTIVITY_SUMMARY_PATH_BY_DEVICE = "/api/historical/device/{device_id}/activity-summary"
ACTIVITY_SUMMARY_PATH_BY_USER = "/api/historical/user/{user_id}/activity-summary"
ATTENTION_LEVEL_SUMMARY_PATH_BY_USER = "/api/historical/user/{user_id}/attention-level-summary"
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


@mcp.tool()
async def get_activity_summary_by_device(
    device_id: str,
    start_time: str,
    end_time: str,
    group_by: str | None = None,
) -> dict:
    """Get summarized activity for a device and time range.

    Args:
        device_id: Device ID
        start_time: start of window (ISO8601 string)
        end_time: end of window (ISO8601 string)
        group_by: optional grouping dimension (e.g. `day`)
    """
    params: dict[str, object] = {
        "start_time": start_time,
        "end_time": end_time,
    }
    if group_by is not None:
        params["group_by"] = group_by

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            ACTIVITY_SUMMARY_PATH_BY_DEVICE.format(device_id=device_id),
            params=params,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_activity_summary_by_user(
    user_id: str,
    start_time: str,
    end_time: str,
    group_by: str | None = None,
) -> dict:
    """Get summarized activity for a user and time range.

    Args:
        user_id: User ID
        start_time: start of window (ISO8601 string)
        end_time: end of window (ISO8601 string)
        group_by: optional grouping dimension (e.g. `day`)
    """
    params: dict[str, object] = {
        "start_time": start_time,
        "end_time": end_time,
    }
    if group_by is not None:
        params["group_by"] = group_by

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            ACTIVITY_SUMMARY_PATH_BY_USER.format(user_id=user_id),
            params=params,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_attention_level_summary_by_user(
    user_id: str,
    start_time: str,
    end_time: str,
    group_by: list[Literal[GroupByQuery.DAY, GroupByQuery.HOUR]],
) -> dict:
    """Get summarized attention level and productivity for a user and time range.

    Args:
        user_id: User ID
        start_time: start of window (ISO8601 string)
        end_time: end of window (ISO8601 string)
        group_by: grouping dimension (e.g. `day`, 'hour)
    """
    params: dict[str, object] = {
        "start_time": start_time,
        "end_time": end_time,
    }

    if group_by:
        converted_group_by: list[str] = []
        for g in group_by:
            if isinstance(g, Enum):
                converted_group_by.append(g.value)
            else:
                converted_group_by.append(str(g))
        params["group_by"] = converted_group_by

    async with httpx.AsyncClient(base_url=settings.backend_base_url, follow_redirects=True) as client:
        resp = await client.get(
            ATTENTION_LEVEL_SUMMARY_PATH_BY_USER.format(user_id=user_id),
            params=params,
        )
        resp.raise_for_status()
        return resp.json()
