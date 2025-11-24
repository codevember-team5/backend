# Codevember Team5 - Backend



## Installation

Install poetry:

```bash
  curl -sSL https://install.python-poetry.org | python3 -
```

Install project dependencies:

```bash
  make install
```

Install dev dependencies and enable pre-commit hooks:

```bash
  make install-dev
```

## Running the Application

Start the server:

```bash
  make run
```

## Developers

Run linting:

```bash
  make lint
```

MongoDB Tables:
['devices', 'users', 'process_windows', 'activity_logs']


## Project Structure

```
src/
├── common/                # Reusable utilities and shared logic
│   └── exceptions.py      # Application-wide custom exceptions
│
├── database/              # Database configuration and connection handling
│   └── database.py        # MongoDB client setup and access utilities
│
├── entrypoints/           # Application entrypoints (e.g., REST API)
│   └── rest/
│       ├── server.py      # FastAPI/Uvicorn app initialization
│       ├── routers/       # Route definitions grouped by feature
│       └── schemas/       # Pydantic request/response models
│
├── user/                  # "User" domain logic
│   ├── domain/            # Domain models and mappers
│   ├── repository.py      # Persistence layer for user data
│   └── service.py         # Business logic for user operations
│
├── historical/            # "Historical" domain logic
│   ├── domain/            # Domain models or domain utilities
│   ├── repository.py      # Persistence layer for historical data
│   └── service.py         # Business logic
│
├── services/              # Shared services used across domains
│
├── settings.py            # Application configuration and logging setup
└── ...
```
