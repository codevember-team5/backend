"""Entry point for running the MCP server over stdio transport."""

from src.mcp_server.mcp_server import mcp


def main():
    """Main function to run the MCP server."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
