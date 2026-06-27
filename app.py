#
#   Imports
#

import streamlit as st

# Perso

from views.mainwindow import MainWindow
from database.bootstrap import bootstrap_db

#
#   Init
#

@st.cache_resource
def init():
    """
        All the initializations of the app.

        To be executed only once.
    """
    bootstrap_db()
    return True

#
#   Script
#

def main():
    # Initializing the app
    init()

    # Redering the main window
    MainWindow().render()

if __name__ == "__main__":
    main()