#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View
from helpers.st_session_helper import st_session_helper
from views.bottom_bar.bottom_view import BottomView

#
#   ChatView
#

class ChatView(View):
    """
        Chat view class.
    """

    def render(self) -> None:
        chat_history = st_session_helper.get_st_chat_history()

        for message in chat_history:
            with st.chat_message(message.role):
                st.write(message.content)

        current_user_input_placeholder = st.empty()

        current_answer_placeholder = st.empty()

        BottomView(
            current_user_input_placeholder,
            current_answer_placeholder,
        ).render()