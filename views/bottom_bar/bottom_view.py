#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View
from views.bottom_bar.chat_bar_view import ChatBarView

#
#   BottomView
#

class BottomView(View):
    """
        Bottom bar for the application.
    """

    def __init__(
        self,
        current_user_input_placeholder, # type: ignore
        current_answer_placeholder, # type: ignore
    ):
        self._current_user_input_placeholder = current_user_input_placeholder # type: ignore
        self._current_answer_placeholder = current_answer_placeholder # type: ignore

    #
    #   Methods
    #
    
    def style_bottom_bar(self) -> None:
        """
            Style the bottom bar for the application.
        """
        st.markdown("""
            <style>
                [data-testid="stBaseButton-secondary"] {
                    width: 100%;
                    height: 100%;
                    background:
                        linear-gradient(
                            135deg,
                            rgba(20, 184, 255, 0.22) 0%,
                            rgba(20, 184, 255, 0.25) 40%,
                            rgba(20, 184, 255, 0.12) 100%
                        );
                    border: 1px solid rgba(20, 184, 255, 0.60);
                    box-shadow: 0 0 18px rgba(20, 184, 255, 0.10);
                }
            </style>
            """, unsafe_allow_html=True)

    #
    #   Overrides
    #
    
    def render(self) -> None:
        self.style_bottom_bar()
        
        with st.bottom:
            col1, col2 = st.columns(
                [1, 8],
                vertical_alignment="center",
            )

            with col1:
                st.button("", icon=":material/mic:")

            with col2:
                ChatBarView(
                    self._current_user_input_placeholder, # type: ignore
                    self._current_answer_placeholder # type: ignore
                ).render()

