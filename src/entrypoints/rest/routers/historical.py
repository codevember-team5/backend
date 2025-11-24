"""User Router Module."""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status

from src.entrypoints.rest.schemas.historical import GetActivitiesLogsResponse
from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.historical.repository import BeanieHistoricalRepository
from src.historical.service import HistoricalService

# router definition
router = APIRouter(prefix="/historical", tags=["Historical"])


def historical_service_factory() -> HistoricalService:
    """User service factory."""
    return HistoricalService(repository=BeanieHistoricalRepository())


@router.get(
    "/device/{device_id}/activities-logs",
    summary="Get All Activity Logs for a Device",
    response_model=GetActivitiesLogsResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the list of Activity Logs for the specified device",
            "model": GetActivitiesLogsResponse,
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
async def get_activities_logs_by_device_id(
    device_id: str,
    skip: int | None = Query(default=None, ge=0),
    limit: int | None = Query(default=None, ge=1, le=200),
    start_time: datetime | None = Query(default=None),
    stop_time: datetime | None = Query(default=None),
    historical_service: HistoricalService = Depends(historical_service_factory),
) -> GetActivitiesLogsResponse:
    """Get Activities Logs by Device."""
    activities_logs = await historical_service.get_activities_log_by_device(
        device_id=device_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        stop_time=stop_time,
    )
    return GetActivitiesLogsResponse(activities_logs=activities_logs)


@router.get(
    "/user/{user_id}/activities-logs",
    summary="Get All Activity Logs for a User",
    response_model=GetActivitiesLogsResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the list of Activity Logs for the specified user",
            "model": GetActivitiesLogsResponse,
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
async def get_activities_logs_by_user_id(
    user_id: str,
    skip: int | None = Query(default=None, ge=0),
    limit: int | None = Query(default=None, ge=1, le=200),
    start_time: datetime | None = Query(default=None),
    stop_time: datetime | None = Query(default=None),
    historical_service: HistoricalService = Depends(historical_service_factory),
) -> GetActivitiesLogsResponse:
    """Get Activities Logs by User."""
    activities_logs = await historical_service.get_activities_log_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        stop_time=stop_time,
    )
    return GetActivitiesLogsResponse(activities_logs=activities_logs)
