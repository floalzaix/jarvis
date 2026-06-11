#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View

#
#   ToolsView
#

class ToolsView(View):
    """
        Tools view for the application.
    """

    #
    #   Methods
    #
    
    def style_tools_view(self) -> None:
        """
            Style the tools view for the application.
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
        self.style_tools_view()
        st.button("", icon=":material/mic:")