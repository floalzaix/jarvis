#
#   Imports
#

from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

#
#   Functions
#

def get_system_prompt() -> str:
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

#
#   Enums
#

class Env(str, Enum):
    """
        The environment of the app.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"

#
#   Configuration
#

class Settings(BaseSettings):
    """
        Handles all the global settings from the app. It loads it
        from the .env file at the root of the project.

        It also reads the files like the prompts to provide the content.
    """

    #
    #   Environment
    #
    
    APP_ENV: str = Field(
        default="development",
        description="Wether the app is in prod or dev mode"
    )

    #
    #   Model settings
    #
    
    MODEL: str = Field(
        default="qwen3:8b",
        description="The model to use for the LLM"
    )

    THINK: bool = Field(
        default=False,
        description="Whether to enable thinking for the LLM"
    )

    #
    #   Prompts
    #
    
    SYSTEM_PROMPT: str = Field(
        default_factory=get_system_prompt,
        description="The system prompt for the LLM"
    )

    #
    #   Database
    #
    
    DATABASE_URL: str = Field(
        default="sqlite:///jarvis_memory.db",
        description="""
            The URL of the database to use.
            It can be a SQLite, MySQL, PostgreSQL, or other supported database.
            The default is a SQLite database in the current directory.
        """
    )

    #
    #   Config
    #
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid"
    )

#
#   Functions
#

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()  # type: ignore[call-arg]