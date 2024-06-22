__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card
from ...view.Graphics import Graphics


class HumanPlayer(Player):
    """HumanPlayer class for the Skull King game"""

    def __init__(self, name:str, graphics:Graphics) -> None:
        super().__init__(name=name)
        self.__graphics = graphics
    
    def choose_card(self, requested_color:str) -> "Card":
        playable_cards = self.playable_cards(requested_color)
        if len(playable_cards) == 0:
            playable_cards = self._hand
        return self.__graphics.choose_card(self._hand, playable_cards)
    
    def place_bet(self) -> int:
        return self.__graphics.place_bet(self._hand)

