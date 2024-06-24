__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from ..cards.Card import Card
from ..cards.CardCollection import CardCollection

import random
import time
from typing import Dict, Any


class RandomPlayer(ComputerPlayer):
    """Random Player class for the Skull King game, simulates a player that plays randomly"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name, delay=delay)
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        time.sleep(self._delay)
        playable_cards = self.playable_cards(features["trick"].requested_color())
        return playable_cards[0]
    
    def place_bet(self) -> int:
        time.sleep(self._delay)
        return random.randint(0, len(self.hand))