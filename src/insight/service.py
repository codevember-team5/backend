"""Service layer for insight generation."""

from datetime import UTC
from datetime import datetime
from datetime import timedelta

from src.services.ai_service import AIService
from src.user.repository import BeanieUserRepository
from src.user.service import UserService


class InsightService:
    """Service layer responsible for generating insights."""

    def __init__(self):
        """Initialize the InsightService with user and AI dependencies."""
        self.user_service = UserService(BeanieUserRepository())
        self.ai_service = AIService()

    async def get_productivity_insights(self, device_id: str, last_n_days: int = 3) -> str:
        """Get productivity insights for a given device."""
        agent = await self.ai_service.get_ai_agent()

        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(days=last_n_days)

        start_iso = start_time.isoformat().replace("+00:00", "Z")
        end_iso = end_time.isoformat().replace("+00:00", "Z")

        prompt = f"""
            Sei un assistente che ha accesso a diversi tool MCP per leggere i dati storici
            di attività dei device.

            Obiettivo:
            Analizzare la produttività del device con id "{device_id}" degli ultimi {last_n_days} giorni.
            Devi passare i seguenti parametri al tool:
               - device_id = "{device_id}"
               - start_time = "{start_iso}"
               - end_time = "{end_iso}"
               - group_by = "day"

            Output:
            Restituisci SOLO una frase che dice quanto tempo è stato utilizzato il device con id {device_id}.
            """

        result = await agent.a_run(prompt)

        return result.text
