#
#   Imports
#

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
#   Configuration
#

class Settings(BaseSettings):
    """
        Handles all the global settings from the app. It loads it
        from the .env file at the root of the project.

        It also reads the files like the prompts to provide the content.
    """

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