__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Player import Player
from ..cards.Card import Card
from ..cards.CardCollection import CardCollection

from abc import abstractmethod
from typing import Dict, Any


class ComputerPlayer(Player):
    """Abstract Player class for all the computer players in the Skull King game"""
    
    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name)
        self._delay = delay
    
    @abstractmethod
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        pass
    
    @abstractmethod
    def place_bet(self) -> int:
        pass