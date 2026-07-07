#
#   Imports
#

# Perso

from helpers.st_session_helper import STSessionHelper
from views.mainwindow import MainWindow

#
#   Script
#

def main():
    #
    #   Init
    #
    
    STSessionHelper()

    #
    #   UI
    #

    MainWindow().render()

if __name__ == "__main__":
    main()