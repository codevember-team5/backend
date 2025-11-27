"""Insight Domain Model."""

from pydantic import BaseModel


class Insight(BaseModel):
    """Insight Model."""

    id: str
    title: str
    description: str
    value: str


class InsightPrompt(BaseModel):
    """Insight Prompt Generator Model."""

    id: str
    title: str
    description: str
    prompt: str
