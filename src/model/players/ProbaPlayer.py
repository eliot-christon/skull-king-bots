__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from ..cards.Card import Card
from ..cards.CardCollection import CardCollection

from typing import Dict, Any



def P_card_in_trick(card:Card, current_trick:CardCollection, N_occurences_left:int, N_cards_not_played:int, cards_to_play_in_trick:int) -> float:
    if N_occurences_left == 0:
        return 0.
    if card in current_trick:
        return 1.
    return cards_to_play_in_trick * N_occurences_left / N_cards_not_played

class ProbaPlayer(ComputerPlayer):
    """Proba Player class for the Skull King game, simulates a player that plays taking into account the probability of winning the trick"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name, delay=delay)
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        pass
    
    def place_bet(self) -> int:
        pass
    
    def proba_of_winning_trick(self, current_trick:CardCollection, card:Card) -> float:
        """Returns the probability of winning the trick if the player plays the given card"""
        pass