__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Graphics import Graphics
from ..model.Game import Game
from ..model.cards.Card import Card
from ..model.cards.CardCollection import CardCollection

from typing import List, Dict


class NoGraphics(Graphics):
    """Abstract class for graphics"""

    def __init__(self) -> None:
        super().__init__()
    
    def start_screen(self) -> None:
        """Display the start screen"""
        pass

    def render(self, game:Game) -> None:
        """Render the graphics"""
        # clear the screen
        print("\033c", end="")

    def choose_card_interaction(self, hand:CardCollection, playable_cards:CardCollection) -> "Card":
        """Choose a card from the hand"""
        pass
    
    def place_bet(self, hand:CardCollection) -> int:
        """Place a bet"""
        pass

    def display_history(self, history:List[Dict[str, Dict[str, int]]]) -> None:
        """Display the history of the game in terms of scores, bets and tricks per player per round"""
        pass

