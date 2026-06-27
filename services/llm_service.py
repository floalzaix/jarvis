#
#   Imports
#

import ollama

from typing import List, Optional

# Perso

from config.config import get_settings

#
#   LLM Service
#

SETTINGS = get_settings()

class LLMService:
    """
        LLM Service class.
    """

    def infer(
        self,
        user_input: str,
        history: Optional[List[ollama.Message]] = None,
    ):
        """
            Streams a llm response from the LLM API.

            Here we use a ollama client for a first version of
            the project.

            Params:
                - user_input: The user input to infer.
                - history: The history of the conversation.

            Returns:
                - An iterator of responses from the LLM API.
        """

        #
        #   Validation
        #
        
        assert user_input, "There must be a user input to infer !"

        
        # Creating messages for the AI
        messages: List[ollama.Message] = []
        messages.append(
            ollama.Message(
                role="system",
                content=SETTINGS.SYSTEM_PROMPT
            )
        )
        messages.extend(history or [])
        messages.append(
            ollama.Message(
                role="user",
                content=user_input
            )
        )

        # Infering with the llm model
        stream = ollama.chat( # type: ignore
            model=SETTINGS.MODEL,
            messages=messages,
            think=SETTINGS.THINK,
            stream=True,
        )

        return stream