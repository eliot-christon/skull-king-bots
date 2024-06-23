__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card

import random
import time


class RandomPlayer(Player):
    """ComputerPlayer class for the Skull King game"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name)
        self._delay = delay
    
    def choose_card(self, requested_color:str) -> "Card":
        time.sleep(self._delay)
        playable_cards = self.playable_cards(requested_color)
        return playable_cards[0]
    
    def place_bet(self) -> int:
        time.sleep(self._delay)
        return random.randint(0, len(self.hand))