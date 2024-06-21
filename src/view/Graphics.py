__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from abc import ABC, abstractmethod


class Graphics(ABC):
    """Abstract class for graphics"""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw the graphics"""
        pass

    @abstractmethod
    def update(self) -> None:
        """Update the graphics"""
        pass

    @abstractmethod
    def get_input(self) -> None:
        """Get input"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the graphics"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the graphics"""
        pass

