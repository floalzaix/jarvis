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
        description="Whether the app is in prod or dev mode"
    )

    #
    #   LLM model settings
    #
    
    MODEL: str = Field(
        description="The model to use for the LLM"
    )

    THINK: bool = Field(
        description="Whether to enable thinking for the LLM"
    )

    NB_CTX_TOKENS: int = Field(
        description="""
            The number of context tokens to use for the LLM.
            Careful, this is the total number of tokens that will be
            used for the context. Meaning that this number must be 
            greater than the sum of the number of instruct tokens and
            the number of user tokens and even perhaps a small margin
            of error.
        """
    )

    NB_INSTRUCT_TOKENS: int = Field(
        description="""
            The number of instruct tokens to use for the LLM.
            It includes the system prompt, the skills, the other
            prompts, ...
        """
    )

    NB_HISTORY_TOKENS: int = Field(
        description="""
            Its the number of token left for the user inputs meaning
            the session history, the fact memory and the user_input.
        """
    )

    OLLAMA_PORT: int = Field(
        description="The port of the Ollama server"
    )

    #
    #   Embedder settings
    #
    
    EMBEDDER_MODEL: str = Field(
        description="The model to use for the embedder"
    )

    EMBEDDER_DIM: int = Field(
        description="The dimension of the embedder"
    )

    #
    #   Prompts
    #
    
    SYSTEM_PROMPT: str = Field(
        default_factory=get_system_prompt,
        description="The system prompt for the LLM"
    )

    #
    #   Long term memory
    #
    
    LT_MEMORY_DATABASE_URL: str = Field(
        description="""
            The URL of the database for the long term memory to use.
            It can be a SQLite, MySQL, PostgreSQL, or other supported database.
            The default is a SQLite database in the current directory.
        """
    )

    #
    #   Facts memory
    #
    
    FACTS_MEMORY_DATABASE_URL: str = Field(
        description="""
            The URL of the database for the facts memory to use.
            The default is a Neo4j database at localhost:7687.
        """
    )

    FACTS_MEMORY_USERNAME: str = Field(
        description="The username for the facts memory database"
    )

    FACTS_MEMORY_PASSWORD: str = Field(
        description="The password for the facts memory database"
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