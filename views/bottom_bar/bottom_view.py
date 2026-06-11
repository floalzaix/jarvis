#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View
from views.bottom_bar.chat_view import ChatView
from views.bottom_bar.tools_view import ToolsView

#
#   BottomView
#

class BottomView(View):
    """
        Bottom bar for the application.
    """

    #
    #   Methods
    #
    
    def style_bottom_bar(self) -> None:
        """
            Style the bottom bar for the application.
        """
        st.markdown("""
            <style>
                
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
                ToolsView().render()

            with col2:
                ChatView().render()

