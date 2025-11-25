"""AI service module."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from datapizza.tools.mcp_client import MCPClient

from src.mcp_server.settings import settings as mcp_settings
from src.settings import settings


class AIService:
    """AI service."""

    async def get_ai_agent(self) -> Agent:
        """Asynchronously constructs an AI agent configured with MCP tools and OpenAI.

        This method retrieves the available MCP tools from the MCP server and
        initializes an OpenAI client using the application settings. The resulting
        Agent instance is configured and ready to be used in the application's
        endpoints.

        Returns:
            Agent: A fully configured Datapizza agent.
        """
        mcp_client = MCPClient(url=mcp_settings.backend_base_url + mcp_settings.mcp_base_url)

        mcp_tools = await mcp_client.a_list_tools()

        llm_client = OpenAIClient(api_key=settings.ai_agent.ai_api_key)

        return Agent(
            name="assistant",
            client=llm_client,
            tools=mcp_tools,
        )
