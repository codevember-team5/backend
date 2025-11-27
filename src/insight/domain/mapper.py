"""Mapper functions for User domain model."""

from src.insight.domain.model import Insight
from src.insight.domain.model import InsightPrompt


def insight_prompt_to_insight(prompt: InsightPrompt, result: str) -> Insight:
    """Map Insight Prompt to Insight domain model."""
    return Insight(id=prompt.id, title=prompt.title, description=prompt.description, value=result)
