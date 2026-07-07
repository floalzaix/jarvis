#
#   Imports
#

import ollama
import uuid

from typing import Iterator, List, Optional

# Perso

from services.lt_memory_service import LTMemoryService
from services.llm_service import LLMService
from services.facts_memory_service import FactsMemoryService

from helpers.st_session_helper import st_session_helper

#
#   Chat Controller
#

class ChatController:
    """
        Chat Controller class.
    """

    def __init__(self):
        self._lt_memory_service = LTMemoryService()
        self._facts_memory_service = FactsMemoryService()
        self._llm_service = LLMService()

    def _get_history_from_session(
        self,
        session_id: Optional[uuid.UUID] = None,
    ) -> List[ollama.Message]:
        """
            Gets the history from the session.

            Params:
                - session_id: The id of the session to get
                the history from.

            Returns:
                - The history from the sessio. If the session doesnt
                exists then returns an empty list.

            Raises (for now TODO):
                - DBSessionError: If there is an error when getting
                the history from the database.
        """
        
        return self._lt_memory_service.get_messages_from_session(
            session_id
        ) if session_id else []

    def ask_llm_response(
        self,
        user_input: str,
        user_email: str,
    ) -> Iterator[str]:
        """
            Asks the LLM a response to the user input. It also
            persists the conversation in the database and validates
            the user_input to be correct and the user_email to be valid.
            
            Additionally it updates the chat history for the view before
            waiting for the llm reesponse and after the response is received.

            Params:
                - user_input: The user input to infer.
                - user_email: The email of the user.

            Validations:
                - user_input: none for now TODO.
                - user_email: none for now TODO.

            Raises (for now TODO):
                - ValueError: If the user_input is not correct.
                - UserNotFoundError: If the user_email is not valid.
                - DBSessionError: If there is an error when saving changes
                to the database.

            Returns:
                - An iterator of responses from the LLM API.
        """

        # TODO: Validating user_input and user_email

        # TODO: Handle errors

        user_input_msg = ollama.Message(
            role="user",
            content=user_input
        )

        #
        #   Chat history
        #
        
        session_id = st_session_helper.get_st_chat_session_id()

        chat_history = self._get_history_from_session(session_id)

        stream = self._llm_service.infer(user_input, chat_history)

        session_id = self._lt_memory_service.save_message_to_session(
            user_input_msg,
            user_email,
            session_id
        )

        st_session_helper.set_st_chat_session_id(session_id)

        # Updating the chat history for the view
        chat_history = self._get_history_from_session(session_id)
        st_session_helper.set_st_chat_history(chat_history)

        #
        #   LLM response
        #
        
        full_response = ""
        for response in stream:
            if response.message.content:
                full_response += response.message.content
                yield full_response

        # Saving changes to the session history
        self._lt_memory_service.save_message_to_session(
            ollama.Message(
                role="assistant",
                content=full_response
            ),
            user_email,
            session_id
        )

        # Updating the chat history for the view
        chat_history = self._get_history_from_session(session_id)
        st_session_helper.set_st_chat_history(chat_history)

        return full_response