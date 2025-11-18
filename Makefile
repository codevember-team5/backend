install:
	poetry install --no-root

install-dev:
	poetry install --with dev --no-root
	poetry run pre-commit install

run:
	poetry run uvicorn --reload --host 0.0.0.0 --port 8000 src.entrypoints.rest.server:app

lint:
	poetry run pre-commit run --all-files
