__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from ..cards.Card import Card

import random
import time


class RandomPlayer(ComputerPlayer):
    """Random Player class for the Skull King game, simulates a player that plays randomly"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name, delay=delay)
    
    def choose_card(self, requested_color:str) -> "Card":
        time.sleep(self._delay)
        playable_cards = self.playable_cards(requested_color)
        return playable_cards[0]
    
    def place_bet(self) -> int:
        time.sleep(self._delay)
        return random.randint(0, len(self.hand))