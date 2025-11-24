"""Health Router Module."""

import time

from datetime import timedelta

from fastapi import APIRouter
from starlette import status

from src.entrypoints.rest.schemas.health import GetHealthResponse

# router definition
router = APIRouter(prefix="/health", tags=["Health"])

START_TIME = time.time()


@router.get(
    "/",
    summary="Get Health Check",
    response_model=GetHealthResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns health status",
        },
    },
)
async def get_health() -> GetHealthResponse:
    """Get health status of the application."""
    uptime_seconds = time.time() - START_TIME
    uptime = str(timedelta(seconds=int(uptime_seconds)))
    return GetHealthResponse(status="ok", uptime=uptime)
