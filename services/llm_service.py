#
#   Imports
#

import ollama

from typing import List, Optional

# Perso

from models.inference_payload import InferencePayload
from config.config import get_settings

#
#   LLM Service
#

SETTINGS = get_settings()

class LLMService:
    """
        LLM Service class.
    """

    #
    #   Methods
    #

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

        assert user_input, "There must be a user input to infer !"

        payload = InferencePayload()
        payload.add_history_inputs(history or [])
        payload.add_history_input(
            ollama.Message(
                role="user",
                content=user_input
            )
        )

        # Infering with the llm model
        stream = ollama.chat( # type: ignore
            model=SETTINGS.MODEL,
            messages=payload.get_content(),
            think=SETTINGS.THINK,
            stream=True,
            options={
                "num_ctx": SETTINGS.NB_CTX_TOKENS,
            }
        )

        return stream