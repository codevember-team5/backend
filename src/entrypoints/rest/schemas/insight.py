"""Insights schemas for REST API."""

from pydantic import BaseModel

from src.insight.domain import model


class GetInsightsResponse(BaseModel):
    """Get insights response schema."""

    insights: list[model.Insight]
