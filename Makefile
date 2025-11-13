
install:
	poetry install --no-root

install-dev:
	poetry install --with dev --no-root
	pre-commit install

run:
	poetry run uvicorn --reload --host 127.0.0.1 --port 8000 src.entrypoints.rest.server:app

lint:
	pre-commit run --all-files
