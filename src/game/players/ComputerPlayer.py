__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card

import random


class ComputerPlayer(Player):
    """ComputerPlayer class for the Skull King game"""

    def __init__(self, name:str) -> None:
        super().__init__(name=name)
    
    def choose_card(self, requested_color:str) -> "Card":
        if len(self.hand.cards_of_color(requested_color)) > 0:
            return self.hand.cards_of_color(requested_color)[0]
        return self.hand[0]
    
    def place_bet(self) -> int:
        return random.randint(0, len(self.hand))