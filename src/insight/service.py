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

    def _build_insight_prompt(
        self,
        user_id: str,
        start_time: datetime,
        stop_time: datetime,
    ) -> list[InsightPrompt]:
        """Costruisce la lista dei prompt di insight da eseguire per un dato utente."""
        intervallo = f"dal {start_time.isoformat()} al {stop_time.isoformat()}"

        return [
            # ---------------------------------------------------------------------
            # 1. INSIGHT: Produttività vs Social / Tempi Persi
            # ---------------------------------------------------------------------
            InsightPrompt(
                id="produttivita_overview",
                title="Produttività e Tempo Perso",
                description="Quanto tempo produttivo ha avuto l'utente e quali social hanno assorbito più tempo.",
                prompt=(
                    "Sei un assistente di produttività con accesso a diversi tool MCP che leggono i dati "
                    "storici dell'utente (es: riepiloghi per categoria, breakdown per applicazione, ecc.).\n\n"
                    "Obiettivo:\n"
                    f"- Analizzare la produttività dell'utente con id '{user_id}' nel periodo {intervallo}.\n"
                    "- Determinare quanto tempo totale ha passato in attività produttive "
                    "(es: CODING, DEVOPS_GIT, DOC_RESEARCH_WORK_WEB, MEETINGS_CALLS).\n"
                    "- Identificare su quali social e app di intrattenimento ha perso più tempo "
                    "e per quanto.\n\n"
                    "Utilizzo dei tool:\n"
                    f"- Quando chiami un tool MCP, passa sempre:\n"
                    f"    user_id = '{user_id}'\n"
                    f"    start_time = '{start_time.isoformat()}'\n"
                    f"    end_time = '{stop_time.isoformat()}'\n"
                    "- Usa skip e limit solo se necessario.\n"
                    "- Basi le tue conclusioni SOLO sui dati restituiti dai tool.\n\n"
                    "Formato output:\n"
                    "- Restituisci UNA SOLA frase, diretta e naturale (nessun bullet point, nessun markdown).\n"
                    "- La frase deve dire:\n"
                    "  1) quanto tempo totale è stato produttivo,\n"
                    "  2) quali social hanno assorbito più tempo e per quanto."
                ),
            ),
            # ---------------------------------------------------------------------
            # 2. INSIGHT: Focus, Deep Work e Finestre di Concentrazione
            # ---------------------------------------------------------------------
            InsightPrompt(
                id="focus_deep_work",
                title="Focus e Finestre di Deep Work",
                description="Concentrazioni e distrazioni dell'utente.",
                prompt=(
                    "Sei un coach di produttività per sviluppatori e knowledge worker.\n"
                    "Hai accesso ai tool MCP che permettono di analizzare i pattern di attività "
                    "per categorie e fasce orarie.\n\n"
                    "Obiettivo:\n"
                    f"- Individuare le finestre di massima concentrazione dell'utente '{user_id}' nel periodo "
                    f"{intervallo}.\n"
                    "- Trovare i momenti con maggiori distrazioni, interruzioni o switching frequente.\n"
                    "- Suggerire come proteggere e ottimizzare le finestre di deep work.\n\n"
                    "Utilizzo dei tool:\n"
                    f"- Passa sempre user_id, start_time ed end_time coerenti: '{user_id}', "
                    f"'{start_time.isoformat()}', '{stop_time.isoformat()}'.\n"
                    "- Analizza metriche come: tempo per categoria, frammentazione delle sessioni, pause.\n\n"
                    "Formato output:\n"
                    "- Restituisci un PARAGRAFO BREVE (2-3 frasi, nessun bullet point).\n"
                    "- Il testo deve:\n"
                    "  1) indicare quando l'utente è più concentrato,\n"
                    "  2) quando si distrae di più,\n"
                    "  3) dare 1-2 consigli pratici per migliorare il deep work."
                ),
            ),
            # ---------------------------------------------------------------------
            # 3. INSIGHT: Bilanciamento, Pause e Rischio Sovraccarico
            # ---------------------------------------------------------------------
            InsightPrompt(
                id="bilanciamento_pause_overload",
                title="Bilanciamento, Pause e Rischio Sovraccarico",
                description="Insight su equilibrio, pause, orari di lavoro e possibili segnali di sovraccarico.",
                prompt=(
                    "Sei un coach orientato al benessere e al bilanciamento lavoro/vita.\n"
                    "Hai accesso ai tool MCP che possono mostrarti pause, sessioni continue, "
                    "orari di lavoro e categorie di inattività.\n\n"
                    "Obiettivo:\n"
                    f"- Analizzare l'equilibrio generale dell'utente '{user_id}' nel periodo {intervallo}.\n"
                    "- Identificare:\n"
                    "    • sessioni molto lunghe senza pause,\n"
                    "    • lavoro ripetuto in tarda serata,\n"
                    "    • giornate con attività significativamente più alte della media.\n"
                    "- Valutare se ci sono segnali di sovraccarico o rischio burnout.\n"
                    "- Suggerire piccoli miglioramenti realistici.\n\n"
                    "Utilizzo dei tool:\n"
                    f"- Passa sempre user_id, start_time ed end_time: '{user_id}', '{start_time.isoformat()}', "
                    f"'{stop_time.isoformat()}'.\n"
                    "- Considera la categoria BREAK_IDLE e la distribuzione oraria.\n\n"
                    "Formato output:\n"
                    "- Restituisci un PARAGRAFO BREVE (2-4 frasi, nessun elenco).\n"
                    "- Il testo deve:\n"
                    "  1) indicare se il bilanciamento sembra sano o meno,\n"
                    "  2) evidenziare eventuali segnali di rischio,\n"
                    "  3) proporre 1-2 suggerimenti concreti e sostenibili."
                ),
            ),
        ]
