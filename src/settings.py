"""Application settings module."""

import sys

from loguru import logger
from pydantic import Field

from src.common.shared import CommonSettings


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
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    def __init__(self, *args, **kwargs) -> None:
        """Init settings."""
        super().__init__(*args, **kwargs)
        self._set_log_level()

    def _set_log_level(self):
        try:
            logger.remove(0)
        except ValueError:
            logger.debug("No default logger found, already removed")
        try:
            # create only one logger sink, if not already created
            if not logger._core.handlers:  # noqa: SLF001
                logger.add(sys.stderr, level=self.log_level)
                logger.debug(f"Logger initialized in this component with log level: {self.log_level}")
            else:
                logger.debug("Logger already initialized in another component, use that one")
        except ValueError:
            logger.exception("Error setting log level")


def get_logger():  # noqa: ANN201
    """Get logger."""
    return logger


settings = Settings()
