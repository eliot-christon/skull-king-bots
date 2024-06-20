__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card


class HumanPlayer(Player):
    """HumanPlayer class for the Skull King game"""

    def __init__(self, name:str) -> None:
        super().__init__(name=name)
    
    def choose_card(self) -> "Card":
        print("Choose a card to play.")
        print(self._hand)
        card = input("Enter the index of the card you want to play: ")
        return self._hand[int(card)]

