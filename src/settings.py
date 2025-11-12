from fastapi.logger import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

class DatabaseSettings(CommonSettings):
    """Database related settings.

    Args:
        BaseSettings (BaseSettings): pydantic BaseSettings class
    """

    uri: str = Field("localhost", validation_alias="MONGO_URI")
    dbname: str = Field("dbname", validation_alias="MONGO_DB")


class Settings(CommonSettings):
    """Application settings.

    Args:
        BaseSettings (BaseSettings): pydantic BaseSettings class
    """
    
    db: DatabaseSettings = DatabaseSettings()
    debug: bool = Field(False, validation_alias="DEBUG")
    wait_for_debugger_connected: bool = Field(False, validation_alias="WAIT_FOR_DEBUGGER")


    def __init__(self, *args, **kwargs) -> None:
        """Init settings."""
        super().__init__(*args, **kwargs)
    


def get_logger():  # noqa: ANN201
    """Get logger."""
    return logger

settings = Settings()