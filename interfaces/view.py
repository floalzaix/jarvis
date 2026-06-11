#
#   Imports
#

from abc import ABC

#
#   View's interface
#

class View(ABC):
    """
        Interface for all the views.
    """

    def render(self) -> None:
        """
            Display the components for the view part.
        """