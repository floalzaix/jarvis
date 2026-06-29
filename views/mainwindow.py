#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View
from views.chat_view import ChatView
from helpers.st_session_helper import st_session_helper

#
#   MainWindow
#

class MainWindow(View):
    """
        Main window for the application.
    """

    #
    #   Methods
    #
    
    def style_background_animation(self) -> None:
        """
            AI generated background animation to
            seem like a in the movie.
        """
        st.markdown("""
            <style>
                .stApp {
                    position: relative;
                    background-image: url("/app/static/images/jarvis_background.png");
                    background-repeat: no-repeat;
                    background-position: center center;
                    background-size: cover;
                    overflow: hidden;
                }

                .stApp::before {
                    content: "";
                    position: fixed;
                    inset: 0;
                    background-image: url("/app/static/images/jarvis_background_blurry.png");
                    background-repeat: no-repeat;
                    background-position: center center;
                    background-size: cover;
                    opacity: """ + ("1" if st_session_helper.get_st_chat_history() else "0") + """;
                    transition: opacity 2s ease;
                    pointer-events: none;
                    z-index: 0;
                }

                .stApp > * {
                    position: relative;
                    z-index: 1;
                }

                """

                +

                """

                .stApp {
                    animation: appFadeIn 5s ease-in-out both;
                }

                @keyframes appFadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }
            </style>
            """, unsafe_allow_html=True)

    def set_page_config(self) -> None:
        """
            Set the configurations of the page such as the title
            and the icon on top of the outlet.
        """
        st.set_page_config(
            page_title="J.A.R.V.I.S",
            page_icon="/app/static/images/jarvis_logo.png",
        )


    #
    #   Overrides
    #
    
    def render(self) -> None:
        self.style_background_animation()
        self.set_page_config()
        ChatView().render()