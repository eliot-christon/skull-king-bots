__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from ..model.Game import Game

from abc import ABC, abstractmethod
import time


class Graphics(ABC):
    """Abstract class for graphics"""

    def __init__(self, game:Game) -> None:
        self._game = game

    @abstractmethod
    def render(self) -> None:
        """Render the graphics"""
        pass

