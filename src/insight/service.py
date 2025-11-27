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

    async def get_productivity_insights_for_device(
        self,
        device_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
    ) -> str:
        """Get productivity insights for a given device."""
        agent = await self.ai_service.get_ai_agent()

        if start_time is None or stop_time is None:
            now = datetime.now(UTC)
            start_utc = now - timedelta(days=30)
            stop_utc = now

        start_iso = start_utc.isoformat().replace("+00:00", "Z")
        stop_iso = stop_utc.isoformat().replace("+00:00", "Z")

        prompt = (
            "Sei un assistente che ha accesso a diversi tool MCP per leggere i dati storici "
            "di attività dei device.\n"
            "Obiettivo:\n"
            f'Analizzare la produttività del device con id "{device_id}" '
            f"nel periodo tra {start_iso} e {stop_iso}.\n"
            "Devi passare i seguenti parametri al tool:\n"
            f'   - device_id = "{device_id}"\n'
            f'   - start_time = "{start_iso}"\n'
            f'   - end_time = "{stop_iso}"\n'
            f"   - skip = {skip}\n"
            f"   - limit = {limit}\n"
            '   - group_by = "day"\n\n'
            "Output:\n"
            f"Restituisci SOLO una frase che riassume quanto tempo il device con id {device_id} è stato utilizzato."
        )

        result = await agent.a_run(prompt)

        return result.text

    async def get_productivity_insights_for_user(
        self,
        user_id: str,
        skip: int | None = None,
        limit: int | None = None,
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
    ) -> str:
        """Get productivity insights for a given user."""
        agent = await self.ai_service.get_ai_agent()

        if start_time is None or stop_time is None:
            now = datetime.now(UTC)
            start_utc = now - timedelta(days=3)
            stop_utc = now

        start_iso = start_utc.isoformat().replace("+00:00", "Z")
        stop_iso = stop_utc.isoformat().replace("+00:00", "Z")

        prompt = (
            "Sei un assistente che ha accesso a diversi tool MCP per leggere i dati storici "
            "di attività degli utenti.\n"
            "Obiettivo:\n"
            f"Analizzare la produttività dell'utente con id {user_id}"
            f"nel periodo tra {start_iso} e {stop_iso}.\n"
            "Devi passare i seguenti parametri al tool:\n"
            f"   - user_id = {user_id}\n"
            f"   - start_time = {start_iso}\n"
            f"   - end_time = {stop_iso}\n"
            f"   - skip = {skip}\n"
            f"   - limit = {limit}\n"
            "- 'skip' indica quanti record saltare all'inizio (paginazione).\n"
            "- 'limit' indica quanti record massimi leggere.\n\n"
            "Output:\n"
            f"Restituisci SOLO una frase che dice quanto tempo l'utente con id {user_id} è stato produttivo."
        )

        result = await agent.a_run(prompt)

        return result.text
