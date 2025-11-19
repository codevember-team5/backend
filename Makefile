install:
	poetry install --without dev --no-root

install-dev:
	poetry install --with dev --no-root
	poetry run pre-commit install

run:
	poetry run uvicorn --reload --host 0.0.0.0 --port 8000 src.entrypoints.rest.server:app

run-only-http-mcp-server:
	poetry run python -m src.mcp_server.entrypoints.http_main

lint:
	poetry run pre-commit run --all-files

mcp-server-inspector:
	docker run --rm --network host -p 6274:6274 -p 6277:6277 ghcr.io/modelcontextprotocol/inspector:latest
