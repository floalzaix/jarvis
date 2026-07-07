#
#   Imports
#

import ollama
import tiktoken

from typing import List, Optional

# Perso

from config.config import get_settings

#
#   Errors
#

class TokenCountError(Exception):
    """
        Exception raised when the token count is not valid.
    """
    def __init__(
        self,
        message: str,
    ):
        self.message = message
        super().__init__(self.message)

#
#   LLM Service
#

SETTINGS = get_settings()

class LLMService:
    """
        LLM Service class.
    """

    def __init__(
        self,
    ):
        # Standard reference encoding for the model but not 
        # exactly the same so margin for error.
        self._encoding = tiktoken.get_encoding("cl100k_base")

    def _get_token_count(
        self,
        messages: List[ollama.Message],
    ) -> int:
        """
            Gets the number of tokens in a text.
        """
        rendered_messages = ""
        for message in messages:
            rendered_messages += f"<|{message.role}|>\n{message.content}\n"

        return len(self._encoding.encode(rendered_messages))

    def _validate_token_count(
        self,
        instructs: List[ollama.Message],
        history: List[ollama.Message],
    ):
        """
            Validates the token count of the messages.

            Meaning that it calculates the total number of tokens 
            for the instructs, the history, and then check if the
            each number respects the limits in the settings.

            Additionnaly, it checks if the total number of tokens is
            greater than the number of context tokens. But that should
            not happen since it is a setting to be set to a value greater
            than the sum of the number of instruct tokens and the number
            of user tokens in the .env config file.

            Params:
                - instructs: The instructs (prompts, skills, ...) to validate.
                - history: The history (session history, fact memory, ...)
                to validate.

            Returns:
                - True if the token count is valid, False otherwise.

            Raises:
                - RuntimeError: If the sum of the token exceeds the total
                number of tokens as it should not happen.
        """

        # Calculating the total number of tokens
        instructs_tokens = self._get_token_count(instructs)
        history_tokens = self._get_token_count(history)
        total_tokens = instructs_tokens + history_tokens

        # Checking if the total number of tokens exceeds
        # the total number of tokens as it should not happen
        if total_tokens > SETTINGS.NB_CTX_TOKENS:
            raise RuntimeError(f"""
                The total number of tokens
                exceeds the total number of tokens as it should not
                happen: {total_tokens} > {SETTINGS.NB_CTX_TOKENS}
                with the instructs tokens: {instructs_tokens} and
                the history tokens: {history_tokens}
            """)

        return (
            history_tokens <= SETTINGS.NB_USER_TOKENS and
            instructs_tokens <= SETTINGS.NB_INSTRUCT_TOKENS
        )


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
        instructs: List[ollama.Message] = []
        instructs.append(
            ollama.Message(
                role="system",
                content=SETTINGS.SYSTEM_PROMPT
            )
        )
        
        user_history: List[ollama.Message] = []
        user_history.extend(history or [])
        user_history.append(
            ollama.Message(
                role="user",
                content=user_input
            )
        )

        # Validating the token count
        if not self._validate_token_count(instructs, user_history):
            instructs_tokens = self._get_token_count(instructs)
            user_history_tokens = self._get_token_count(user_history)

            raise TokenCountError(f"""
                The token count is not valid
                -> Instructs tokens:
                {instructs_tokens} / {SETTINGS.NB_INSTRUCT_TOKENS}
                -> User history tokens:
                {user_history_tokens} / {SETTINGS.NB_USER_TOKENS}
            """)

        #
        #   Infering with the llm model
        #

        stream = ollama.chat( # type: ignore
            model=SETTINGS.MODEL,
            messages=instructs + user_history,
            think=SETTINGS.THINK,
            stream=True,
            options={
                "num_ctx": SETTINGS.NB_CTX_TOKENS,
            }
        )

        return stream