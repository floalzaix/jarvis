#
#   Imports
#

import tiktoken
import ollama

from typing import List, ClassVar

# Perso

from config.config import get_settings
from helpers.st_session_helper import st_session_helper

#
#   Inference Payload Class
#

SETTINGS = get_settings()

class InferencePayload:
    """
        Class to represent the payload of an inference.

        It solves the issue of counting the tokens used for
        each inference as some messages maybe added or removed
        which then triggers a change in the token count, keeping
        track while maintaining a clear structure.

        Class variables:
            - _encoding: The encoding to use for the tokens.

        Instance variables:
            - _instructs:
                The instructs to the model.
                This is the system prompt, the skills, ...
                This includes also some small extensions or rules
                and other small stuff.
            - _history_inputs:
                The history of the conversation with the model.
                This is the history of the conversation with the model.
                But also the history from the fact memory, ...

    """

    #
    #   Class variables
    #
    
    _encoding: ClassVar[tiktoken.Encoding] = tiktoken.get_encoding("cl100k_base")

    #
    #   Constructor
    #

    def __init__(self):
        self._instructs: List[ollama.Message] = [
            ollama.Message(role="system", content=SETTINGS.SYSTEM_PROMPT)
        ]
        self._history_inputs: List[ollama.Message] = []

    #
    #   Methods
    #

    @classmethod
    def _get_token_count(
        cls,
        messages: List[ollama.Message],
    ) -> int:
        """
            Gets the number of tokens in a List of
            ollama.Message.

            It counts the number of tokens in the total
            meaning it sums every token count of each message.
        """
        rendered_messages = ""
        for message in messages:
            rendered_messages += f"<|{message.role}|>\n{message.content}\n"

        return len(cls._encoding.encode(rendered_messages))

    def _make_user_input_window(self):
        """
            Makes the history window smaller if it exceeds the
            number of tokens allowed for the history.

            For instance, if the user inputs takes too much tokens
            then it exceeds the number of tokens allowed for the user
            and triggers this function to truncate the user input.

            It simply takes the maximum number of messages but limiting
            the number of tokens fed to the model. Meaning for instance
            if there are 10 messages and an excess of 100 tokens, then it
            will take the last 9 messages and the user input, or even less
            pending on the number of tokens in the messages.

            Returns:
                - A list of messages containing the new user input
                history.
        """

        messages = self._history_inputs.copy()
        messages.reverse()

        kept_messages: List[ollama.Message] = []
        for message in messages:
            message_tokens = self._get_token_count([message])

            if message_tokens + self._get_token_count(
                kept_messages
            ) <= SETTINGS.NB_HISTORY_TOKENS:
                kept_messages.append(message)
            else:
                break

        self._history_inputs = kept_messages

    def _validate_token_count(self) -> None:
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

            It adds a small message to the history inputs to inform the user
            that the session has been truncated if asked to the llm.

            It could also not truncate the history window unless get_content
            is called, this way, perhaps it would be more optimal and
            would permit centralized content management without removing
            the information.

            Raises:
                - RuntimeError: If the sum of the token exceeds the total
                number of tokens as it should not happen.
        """

        # Calculating the total number of tokens
        instructs_tokens = self._get_token_count(
            self._instructs
        )
        history_tokens = self._get_token_count(
            self._history_inputs
        )
        total_tokens = instructs_tokens + history_tokens

        # Checking if the total number of tokens exceeds
        # the total number of tokens as it should not happen
        if (
            SETTINGS.NB_INSTRUCT_TOKENS + SETTINGS.NB_HISTORY_TOKENS >
            SETTINGS.NB_CTX_TOKENS
        ):
            raise RuntimeError(f"""
                The total number of tokens
                exceeds the total number of tokens as it should not
                happen: {total_tokens} > {SETTINGS.NB_CTX_TOKENS}
                with the instructs tokens: {instructs_tokens} and
                the history tokens: {history_tokens}
            """)

        if history_tokens > SETTINGS.NB_HISTORY_TOKENS:
            # Truncating the history window
            pre_length = len(self._history_inputs)
            self._make_user_input_window()
            post_length = len(self._history_inputs)
            nb_cut_session_msgs = pre_length - post_length

            st_session_helper.set_st_nb_cut_session_msgs(
                nb_cut_session_msgs
            )

        
        if st_session_helper.get_st_nb_cut_session_msgs() > 0:
            self._history_inputs.append(
                ollama.Message(
                    role="system",
                    content=f"""
                        The session has been truncated.
                        {st_session_helper.get_st_nb_cut_session_msgs()}
                        firsts messages have been truncated to fit the
                        history window.
                    """
                )
            )

        if instructs_tokens > SETTINGS.NB_INSTRUCT_TOKENS:
            raise RuntimeError(f"""
                The number of instruct tokens exceeds the number of instruct tokens
                as it should not happen:
                {instructs_tokens} > {SETTINGS.NB_INSTRUCT_TOKENS}
                Check the inference payload class as it should handle all the
                instructions for the model and should have almost a static length
                pending on a few parameters.
            """)

        print(f"The number of truncated session messages is: {st_session_helper.get_st_nb_cut_session_msgs()}") # TODO: Remove this

    #
    #   Getters and setters
    #
    
    def add_history_input(self, history: ollama.Message):
        self._history_inputs.append(history)
        self._validate_token_count()

    def add_history_inputs(self, history_inputs: List[ollama.Message]):
        self._history_inputs.extend(history_inputs)
        self._validate_token_count()

    def get_content(self) -> List[ollama.Message]:
        """
            Gets the payload for the inference.
        """
        return self._instructs + self._history_inputs