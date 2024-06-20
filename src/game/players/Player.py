__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from ..cards.CardCollection import CardCollection
from ..cards.Card import Card

from abc import abstractmethod


class Player:
    """Abstract Player class for the Skull King game"""

    def __init__(self, name:str) -> None:
        self._name = name
        self._hand = CardCollection([])
        self._score = 0
    
    def __str__(self) -> str:
        return f"Player: {self._name}, Score: {self._score}, Hand: {self._hand}"
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def hand(self) -> CardCollection:
        return self._hand
    
    @property
    def score(self) -> int:
        return self._score
    
    def add_card(self, card:"Card") -> None:
        self._hand.add(card)
    
    def add_cards(self, cards:CardCollection) -> None:
        self._hand = self._hand + cards
    
    def play_card(self, card:"Card") -> None:
        self._hand.remove(card)
    
    @abstractmethod
    def choose_card(self) -> "Card":
        pass

    def add_score(self, score:int) -> None:
        self._score += score
    
    def reset_hand(self) -> None:
        self._hand.clear()
    