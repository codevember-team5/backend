"""Service layer for insight generation."""

from datetime import datetime

from src.insight.domain.mapper import insight_prompt_to_insight
from src.insight.domain.model import Insight
from src.insight.domain.model import InsightPrompt
from src.services.ai_service import AIService
from src.user.repository import BeanieUserRepository
from src.user.service import UserService


class InsightService:
    """Service layer responsible for generating insights."""

    def __init__(self):
        """Initialize the InsightService with user and AI dependencies."""
        self.user_service = UserService(BeanieUserRepository())
        self.ai_service = AIService()

    async def get_productivity_insights_for_user(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
    ) -> list[Insight]:
        """Get productivity insights for a given user."""
        agent = await self.ai_service.get_ai_agent()

        insights: list[Insight] = []
        for prompt in self._build_insight_prompt(user_id, start_time, stop_time):
            result = await agent.a_run(prompt.prompt)
            insights.append(insight_prompt_to_insight(prompt, result.text))

        return insights

    def _build_insight_prompt(self, user_id: str, start_time: datetime, stop_time: datetime) -> list[InsightPrompt]:
        return [
            InsightPrompt(
                id="produttività",
                title="Insight sulla produttività",
                description="Insight sulla produttività dell'utente",
                prompt=(
                    "Sei un assistente che ha accesso a diversi tool MCP per leggere i dati storici "
                    "di attività degli utenti.\n"
                    "Obiettivo:\n"
                    f"Analizzare la produttività dell'utente con id {user_id}"
                    f"nel periodo tra {start_time} e {stop_time}.\n"
                    "Devi passare i seguenti parametri al tool:\n"
                    f"   - user_id = {user_id}\n"
                    f"   - start_time = {start_time}\n"
                    f"   - end_time = {stop_time}\n"
                    "- 'skip' indica quanti record saltare all'inizio (paginazione).\n"
                    "- 'limit' indica quanti record massimi leggere.\n\n"
                    "Output:\n"
                    f"Prendi il nome dell'utente {user_id} e restituisci SOLO una frase che dice quanto tempo "
                    f"l'utente con id {user_id} è stato produttivo e su quali social ha perso più tempo e quanto "
                    f"per ciascun social."
                ),
            ),
        ]
