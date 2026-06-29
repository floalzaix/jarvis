#
#   Imports
#

import streamlit as st

# Perso

from interfaces.view import View
from controllers.chat_controller import ChatController

#
#   View
#

class ChatBarView(View):
    """
        View for the chat interface.
    """

    def __init__(
        self,
        current_user_input_placeholder, # type: ignore
        current_answer_placeholder, # type: ignore
    ):
        self._current_user_input_placeholder = current_user_input_placeholder # type: ignore
        self._current_answer_placeholder = current_answer_placeholder # type: ignore
        self.chat_controller = ChatController()

    #
    #   Methods
    #
    
    def style_chat_inputs(self) -> None:
        """
            Style the chat inputs.
        """
        st.markdown("""
            <style>

            [data-testid="stChatMessageAvatarUser"] {
                background-color: #1d4ed8 !important;
                color: white !important;
            }

            [data-testid="stChatMessageAvatarAssistant"] {
                background-color: #0f766e !important;
                color: white !important;
            }

            [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
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

            /* Jarvis ring effect */

            @property --ring-x {
                syntax: '<percentage>';
                inherits: false;
                initial-value: 50%;
            }

            @property --ring-y {
                syntax: '<percentage>';
                inherits: false;
                initial-value: 50%;
            }

            @property --ring-amplitude-x {
                syntax: '<percentage>';
                inherits: false;
                initial-value: 4%;
            }

            @property --ring-amplitude-y {
                syntax: '<percentage>';
                inherits: false;
                initial-value: 4%;
            }

            [data-testid="stAppViewContainer"] {
                --ring-amplitude-x: 3%;
                --ring-amplitude-y: 30%;

                background:
                    radial-gradient(
                        circle at var(--ring-x) var(--ring-y),
                        rgba(20, 184, 255, 0.0) 0%,
                        rgba(20, 184, 255, 0.0) 70%,
                        rgba(20, 184, 255, 0.45) 74%,
                        rgba(20, 184, 255, 1) 75%,
                        rgba(20, 184, 255, 1) 76%,
                        rgba(20, 184, 255, 0.45) 77%,
                        rgba(20, 184, 255, 0.0) 81%,
                        rgba(20, 184, 255, 0.18) 100%
                    );
                background-repeat: no-repeat;
                animation: jarvisOrbit 30s linear infinite;
            }

            @keyframes jarvisOrbit {
                0.00000% { --ring-x: calc(50% + 0.00000 * var(--ring-amplitude-x)); --ring-y: calc(50% + -1.00000 * var(--ring-amplitude-y)); }
                1.56250% { --ring-x: calc(50% + 0.09802 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.99518 * var(--ring-amplitude-y)); }
                3.12500% { --ring-x: calc(50% + 0.19509 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.98079 * var(--ring-amplitude-y)); }
                4.68750% { --ring-x: calc(50% + 0.29028 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.95694 * var(--ring-amplitude-y)); }
                6.25000% { --ring-x: calc(50% + 0.38268 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.92388 * var(--ring-amplitude-y)); }
                7.81250% { --ring-x: calc(50% + 0.47140 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.88192 * var(--ring-amplitude-y)); }
                9.37500% { --ring-x: calc(50% + 0.55557 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.83147 * var(--ring-amplitude-y)); }
                10.93750% { --ring-x: calc(50% + 0.63439 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.77301 * var(--ring-amplitude-y)); }
                12.50000% { --ring-x: calc(50% + 0.70711 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.70711 * var(--ring-amplitude-y)); }
                14.06250% { --ring-x: calc(50% + 0.77301 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.63439 * var(--ring-amplitude-y)); }
                15.62500% { --ring-x: calc(50% + 0.83147 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.55557 * var(--ring-amplitude-y)); }
                17.18750% { --ring-x: calc(50% + 0.88192 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.47140 * var(--ring-amplitude-y)); }
                18.75000% { --ring-x: calc(50% + 0.92388 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.38268 * var(--ring-amplitude-y)); }
                20.31250% { --ring-x: calc(50% + 0.95694 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.29028 * var(--ring-amplitude-y)); }
                21.87500% { --ring-x: calc(50% + 0.98079 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.19509 * var(--ring-amplitude-y)); }
                23.43750% { --ring-x: calc(50% + 0.99518 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.09802 * var(--ring-amplitude-y)); }
                25.00000% { --ring-x: calc(50% + 1.00000 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.00000 * var(--ring-amplitude-y)); }
                26.56250% { --ring-x: calc(50% + 0.99518 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.09802 * var(--ring-amplitude-y)); }
                28.12500% { --ring-x: calc(50% + 0.98079 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.19509 * var(--ring-amplitude-y)); }
                29.68750% { --ring-x: calc(50% + 0.95694 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.29028 * var(--ring-amplitude-y)); }
                31.25000% { --ring-x: calc(50% + 0.92388 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.38268 * var(--ring-amplitude-y)); }
                32.81250% { --ring-x: calc(50% + 0.88192 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.47140 * var(--ring-amplitude-y)); }
                34.37500% { --ring-x: calc(50% + 0.83147 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.55557 * var(--ring-amplitude-y)); }
                35.93750% { --ring-x: calc(50% + 0.77301 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.63439 * var(--ring-amplitude-y)); }
                37.50000% { --ring-x: calc(50% + 0.70711 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.70711 * var(--ring-amplitude-y)); }
                39.06250% { --ring-x: calc(50% + 0.63439 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.77301 * var(--ring-amplitude-y)); }
                40.62500% { --ring-x: calc(50% + 0.55557 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.83147 * var(--ring-amplitude-y)); }
                42.18750% { --ring-x: calc(50% + 0.47140 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.88192 * var(--ring-amplitude-y)); }
                43.75000% { --ring-x: calc(50% + 0.38268 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.92388 * var(--ring-amplitude-y)); }
                45.31250% { --ring-x: calc(50% + 0.29028 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.95694 * var(--ring-amplitude-y)); }
                46.87500% { --ring-x: calc(50% + 0.19509 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.98079 * var(--ring-amplitude-y)); }
                48.43750% { --ring-x: calc(50% + 0.09802 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.99518 * var(--ring-amplitude-y)); }
                50.00000% { --ring-x: calc(50% + 0.00000 * var(--ring-amplitude-x)); --ring-y: calc(50% + 1.00000 * var(--ring-amplitude-y)); }
                51.56250% { --ring-x: calc(50% + -0.09802 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.99518 * var(--ring-amplitude-y)); }
                53.12500% { --ring-x: calc(50% + -0.19509 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.98079 * var(--ring-amplitude-y)); }
                54.68750% { --ring-x: calc(50% + -0.29028 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.95694 * var(--ring-amplitude-y)); }
                56.25000% { --ring-x: calc(50% + -0.38268 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.92388 * var(--ring-amplitude-y)); }
                57.81250% { --ring-x: calc(50% + -0.47140 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.88192 * var(--ring-amplitude-y)); }
                59.37500% { --ring-x: calc(50% + -0.55557 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.83147 * var(--ring-amplitude-y)); }
                60.93750% { --ring-x: calc(50% + -0.63439 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.77301 * var(--ring-amplitude-y)); }
                62.50000% { --ring-x: calc(50% + -0.70711 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.70711 * var(--ring-amplitude-y)); }
                64.06250% { --ring-x: calc(50% + -0.77301 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.63439 * var(--ring-amplitude-y)); }
                65.62500% { --ring-x: calc(50% + -0.83147 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.55557 * var(--ring-amplitude-y)); }
                67.18750% { --ring-x: calc(50% + -0.88192 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.47140 * var(--ring-amplitude-y)); }
                68.75000% { --ring-x: calc(50% + -0.92388 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.38268 * var(--ring-amplitude-y)); }
                70.31250% { --ring-x: calc(50% + -0.95694 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.29028 * var(--ring-amplitude-y)); }
                71.87500% { --ring-x: calc(50% + -0.98079 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.19509 * var(--ring-amplitude-y)); }
                73.43750% { --ring-x: calc(50% + -0.99518 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.09802 * var(--ring-amplitude-y)); }
                75.00000% { --ring-x: calc(50% + -1.00000 * var(--ring-amplitude-x)); --ring-y: calc(50% + 0.00000 * var(--ring-amplitude-y)); }
                76.56250% { --ring-x: calc(50% + -0.99518 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.09802 * var(--ring-amplitude-y)); }
                78.12500% { --ring-x: calc(50% + -0.98079 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.19509 * var(--ring-amplitude-y)); }
                79.68750% { --ring-x: calc(50% + -0.95694 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.29028 * var(--ring-amplitude-y)); }
                81.25000% { --ring-x: calc(50% + -0.92388 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.38268 * var(--ring-amplitude-y)); }
                82.81250% { --ring-x: calc(50% + -0.88192 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.47140 * var(--ring-amplitude-y)); }
                84.37500% { --ring-x: calc(50% + -0.83147 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.55557 * var(--ring-amplitude-y)); }
                85.93750% { --ring-x: calc(50% + -0.77301 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.63439 * var(--ring-amplitude-y)); }
                87.50000% { --ring-x: calc(50% + -0.70711 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.70711 * var(--ring-amplitude-y)); }
                89.06250% { --ring-x: calc(50% + -0.63439 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.77301 * var(--ring-amplitude-y)); }
                90.62500% { --ring-x: calc(50% + -0.55557 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.83147 * var(--ring-amplitude-y)); }
                92.18750% { --ring-x: calc(50% + -0.47140 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.88192 * var(--ring-amplitude-y)); }
                93.75000% { --ring-x: calc(50% + -0.38268 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.92388 * var(--ring-amplitude-y)); }
                95.31250% { --ring-x: calc(50% + -0.29028 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.95694 * var(--ring-amplitude-y)); }
                96.87500% { --ring-x: calc(50% + -0.19509 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.98079 * var(--ring-amplitude-y)); }
                98.43750% { --ring-x: calc(50% + -0.09802 * var(--ring-amplitude-x)); --ring-y: calc(50% + -0.99518 * var(--ring-amplitude-y)); }
                100.00000% { --ring-x: calc(50% + -0.00000 * var(--ring-amplitude-x)); --ring-y: calc(50% + -1.00000 * var(--ring-amplitude-y)); }
            }

            /* Fade effect when scrolling up and down */

            [data-testid="stAppViewContainer"] {
                position: relative;
                overflow: hidden;
            }

            section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"]{
                height: 100%;
                position: relative;
            }

            [data-testid="stAppScrollToBottomContainer"]::before,
            [data-testid="stAppScrollToBottomContainer"]::after{
                content: "";
                position: absolute;
                left: 0;
                right: 0;
                height: 100px;
                pointer-events: none;
                z-index: 10;
            }

            [data-testid="stAppScrollToBottomContainer"]::before{
                top: 0;
                background: linear-gradient(
                    to bottom,
                    rgba(0, 0, 0, 1) 0%,
                    rgba(0, 0, 0, 0) 100%
                );
            }

            [data-testid="stAppScrollToBottomContainer"]::after{
                bottom: 0;
                background:
                    linear-gradient(
                        to top,
                        rgba(0, 0, 0, 1) 0%,
                        rgba(0, 0, 0, 0) 100%
                    ),
                    radial-gradient(
                        circle at 50% 500%,
                        rgba(0, 0, 0, 1) 0%,
                        rgba(0, 0, 0, 1) 60%,
                        rgba(0, 0, 0, 0) 72%,
                        rgba(0, 0, 0, 0) 100%
                    );
            }

            [data-testid="stBottom"] > * {
                background: transparent;
            }

            [data-testid="stChatInputSubmitButton"] {
                background: rgba(20, 184, 255, 0.5) !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    #
    #   Overrides
    #
    
    def render(self) -> None:
        self.style_chat_inputs()
        if user_input := st.chat_input(
            "How can I help you today ?",
        ):

            # Displaying the user input has it is not part of
            # the chat history yet
            with self._current_user_input_placeholder: # type: ignore
                with st.chat_message("user"):
                    st.write(user_input)

            stream = self.chat_controller.ask_llm_response(
                user_input,
                "test@test.com" # TODO: handle users in the ui
            )

            for response in stream:
                with self._current_answer_placeholder: # type: ignore
                    with st.chat_message("assistant"):
                        st.write(response)

            st.rerun()
