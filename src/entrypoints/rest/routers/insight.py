"""API Router for insights."""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from src.insight.service import InsightService

router = APIRouter(prefix="/insight", tags=["Insight"])


def get_insight_service() -> InsightService:
    """Returns the insight service."""
    return InsightService()


@router.get("/productivity/{device_id}")
async def get_productivity_insights_for_device(
    device_id: str,
    skip: int | None = Query(default=None, ge=0),
    limit: int | None = Query(default=None, ge=1, le=200),
    start_time: datetime | None = Query(
        default=None,
        description=(
            "Start of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "00:00 UTC will be used."
        ),
    ),
    stop_time: datetime | None = Query(
        default=None,
        description=(
            "End of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "23:59 UTC will be used."
        ),
    ),
    insight_service: InsightService = Depends(get_insight_service),
) -> str:
    """Endpoint to get productivity insights for a given device."""
    return await insight_service.get_productivity_insights_for_device(
        device_id=device_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        stop_time=stop_time,
    )


@router.get("/productivity/user/{user_id}")
async def get_productivity_insights_for_user(
    user_id: str,
    skip: int | None = Query(default=None, ge=0),
    limit: int | None = Query(default=None, ge=1, le=200),
    start_time: datetime | None = Query(
        default=None,
        description=(
            "Start of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "00:00 UTC will be used."
        ),
    ),
    stop_time: datetime | None = Query(
        default=None,
        description=(
            "End of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "23:59 UTC will be used."
        ),
    ),
    insight_service: InsightService = Depends(get_insight_service),
) -> str:
    """Endpoint to get productivity insights for a given user."""
    return await insight_service.get_productivity_insights_for_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        stop_time=stop_time,
    )
