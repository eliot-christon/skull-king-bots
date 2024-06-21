__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Graphics import Graphics


class ConsoleGraphics(Graphics):
    """ConsoleGraphics class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__()

    def draw(self) -> None:
        """Draw the graphics"""
        pass

    def update(self) -> None:
        """Update the graphics"""
        pass

    def get_input(self) -> None:
        """Get input"""
        pass

    def clear(self) -> None:
        """Clear the graphics"""
        pass

    def close(self) -> None:
        """Close the graphics"""
        pass