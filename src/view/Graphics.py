__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from ..model.Game import Game
from ..model.cards.CardCollection import CardCollection
from ..model.cards.Card import Card

from abc import ABC, abstractmethod
from typing import List, Dict


class Graphics(ABC):
    """Abstract class for graphics"""

    def __init__(self) -> None:
        self._running = True
        
    @property
    def running(self) -> bool:
        return self._running
    
    @abstractmethod
    def start_screen(self) -> None:
        """Display the start screen"""
        pass

    @abstractmethod
    def render(self, game:Game) -> None:
        """Render the graphics"""
        pass

    @abstractmethod
    def choose_card_interaction(self, hand:CardCollection, playable_cards:CardCollection) -> "Card":
        """Choose a card from the hand"""
        pass
    
    @abstractmethod
    def place_bet(self, hand:CardCollection) -> int:
        """Place a bet"""
        pass

    @abstractmethod
    def display_history(self, history:List[Dict[str, Dict[str, int]]]) -> None:
        """Display the history of the game in terms of scores, bets and tricks per player per round"""
        pass

