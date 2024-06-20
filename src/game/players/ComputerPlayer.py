__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card


class ComputerPlayer(Player):
    """ComputerPlayer class for the Skull King game"""

    def __init__(self, name:str) -> None:
        super().__init__(name=name)
    
    def choose_card(self) -> "Card":
        return self._hand[0]