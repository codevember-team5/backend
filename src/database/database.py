# engine
# connessione
# db schema
from pymongo import AsyncMongoClient

from src.settings import settings


def get_db_connection():
    """Get database connection."""
    client = AsyncMongoClient(
        host=settings.db.uri,
    )
    client.get_database(settings.db.dbname)
    return client