__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card
from ..cards.CardCollection import CardCollection
from ...view.Graphics import Graphics

from typing import Dict, Any


class HumanPlayer(Player):
    """HumanPlayer class for the Skull King game"""

    def __init__(self, name:str, graphics:Graphics) -> None:
        super().__init__(name=name)
        self.__graphics = graphics
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        playable_cards = self.playable_cards(features["trick"].requested_color())
        if len(playable_cards) == 0:
            playable_cards = self._hand
        return self.__graphics.choose_card_interaction(self._hand, playable_cards)
    
    def place_bet(self) -> int:
        return self.__graphics.place_bet(self._hand)

