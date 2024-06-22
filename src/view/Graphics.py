__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from ..model.Game import Game
from ..model.cards.CardCollection import CardCollection
from ..model.cards.Card import Card

from abc import ABC, abstractmethod


class Graphics(ABC):
    """Abstract class for graphics"""

    def __init__(self) -> None:
        self._running = True
        
    @property
    def running(self) -> bool:
        return self._running

    @abstractmethod
    def render(self, game:Game) -> None:
        """Render the graphics"""
        pass

    @abstractmethod
    def choose_card(self, hand:CardCollection, playable_cards:CardCollection) -> "Card":
        """Choose a card from the hand"""
        pass
    
    @abstractmethod
    def place_bet(self, hand:CardCollection) -> int:
        """Place a bet"""
        pass

