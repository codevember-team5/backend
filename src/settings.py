from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database related settings.

    Args:
        BaseSettings (BaseSettings): pydantic BaseSettings class
    """

    uri: str = Field("localhost", validation_alias="MONGO_URI")
    dbname: str = Field("dbname", validation_alias="MONGO_DB")


class Settings(BaseSettings):
    """Application settings.

    Args:
        BaseSettings (BaseSettings): pydantic BaseSettings class
    """

    db: DatabaseSettings = DatabaseSettings()

settings = Settings()