"""API Router for insights."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from src.insight.service import InsightService

router = APIRouter(prefix="/insight", tags=["Insight"])


def get_insight_service() -> InsightService:
    """Returns the insight service."""
    return InsightService()


@router.get("/productivity/{device_id}")
async def get_productivity_insights(
    device_id: str,
    last_n_days: int = Query(3, ge=1, le=30),
    insight_service: InsightService = Depends(get_insight_service),
) -> str:
    """Endpoint to get productivity insights for a given device."""
    return await insight_service.get_productivity_insights(device_id=device_id, last_n_days=last_n_days)
