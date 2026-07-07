#
#   Imports
#

import ollama
import uuid
import streamlit as st

from typing import Optional, List

#
#   STSession Helper
#

class STSessionHelper:
    """
        Session Helper class.

        This helper is used to manage the streamlit session
        storage so that this logic is centralized and easy to
        maintain.

        ST session variables:

            - chat_session_id: The id of the current chat session,
            meaning the id of the database chat session that stores
            the history of messages of the current chat session.
    """

    def __init__(self):
        if "chat_session_id" not in st.session_state:
            st.session_state["chat_session_id"] = None

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        if "nb_cut_session_msgs" not in st.session_state:
            st.session_state["nb_cut_session_msgs"] = 0

    def get_st_chat_session_id(self) -> Optional[uuid.UUID]:
        return st.session_state["chat_session_id"]

    def set_st_chat_session_id(self, chat_session_id: uuid.UUID) -> None:
        st.session_state["chat_session_id"] = chat_session_id

    def get_st_chat_history(self) -> List[ollama.Message]:
        return st.session_state["chat_history"]

    def set_st_chat_history(self, chat_history: List[ollama.Message]) -> None:
        st.session_state["chat_history"] = chat_history

    def get_st_has_chat_session(self) -> bool:
        return st.session_state["has_chat_session"]

    def get_st_nb_cut_session_msgs(self) -> int:
        return st.session_state["nb_cut_session_msgs"]

    def set_st_nb_cut_session_msgs(self, nb_cut_session_msgs: int) -> None:
        st.session_state["nb_cut_session_msgs"] = nb_cut_session_msgs

st_session_helper = STSessionHelper()
