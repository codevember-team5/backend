
install:
	poetry install --with dev --no-root

run:
	poetry run uvicorn --reload --host 127.0.0.1 --port 8000 src.entrypoints.rest.server:app