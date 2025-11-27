"""API Router for insights."""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status

from src.entrypoints.rest.schemas.insight import GetInsightsResponse
from src.insight.service import InsightService

router = APIRouter(prefix="/insight", tags=["Insight"])


def get_insight_service() -> InsightService:
    """Returns the insight service."""
    return InsightService()


@router.get(
    "/productivity/user/{user_id}",
    summary="Get Productivity Insights for a User",
    response_model=GetInsightsResponse,
    responses={
        status.HTTP_200_OK: {"description": "Productivity insights retrieved for a given user."},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
    },
)
async def get_productivity_insights_for_user(
    user_id: str,
    start_time: datetime = Query(
        ...,
        description=(
            "Start of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "00:00 UTC will be used."
        ),
    ),
    stop_time: datetime = Query(
        ...,
        description=(
            "End of the time window (ISO8601). "
            "If the time component is omitted and only the date is provided, "
            "23:59 UTC will be used."
        ),
    ),
    insight_service: InsightService = Depends(get_insight_service),
) -> GetInsightsResponse:
    """Endpoint to get productivity insights for a given user."""
    insights = await insight_service.get_productivity_insights_for_user(
        user_id=user_id,
        start_time=start_time,
        stop_time=stop_time,
    )
    return GetInsightsResponse(insights=insights)
