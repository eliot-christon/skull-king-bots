__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card

import random
import time


class ComputerPlayer(Player):
    """ComputerPlayer class for the Skull King game"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name)
        self._delay = delay
    
    def choose_card(self, requested_color:str) -> "Card":
        time.sleep(self._delay)
        if len(self.hand.cards_of_color(requested_color)) > 0:
            return self.hand.cards_of_color(requested_color)[0]
        return self.hand[0]
    
    def place_bet(self) -> int:
        time.sleep(self._delay)
        return random.randint(0, len(self.hand))