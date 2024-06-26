__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from ..cards.Card import Card

import random
import time
from typing import Dict, Any


class TemplateBot(ComputerPlayer):
    """Template Player class for the Skull King game, Coder friendly, follow this template to create your own bot"""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name, delay=delay)
        # you can add your own attributes here
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        t0 = time.time() # to keep track of the time taken by the bot to choose a card
        
        playable_cards = self.playable_cards(features["trick"].requested_color()) # this method is essential to get the playable cards
        
        """You can add your own logic here to choose the best card to play
        Useful functions in src.card.CardCollection.py to help you."""
        
        # delay just before returning the card
        if time.time() - t0 < self._delay:
            time.sleep(self._delay - (time.time() - t0))
        
        # return chosen_card
        raise NotImplementedError("You must implement the choose_card method, do not instantiate the TemplateBot class directly.")
    
    def place_bet(self) -> int:
        t0 = time.time() # to keep track of the time taken by the bot to place a bet
        
        """You can add your own logic here to place the bet similar to the choose_card method"""
        
        # delay just before returning the card
        if time.time() - t0 < self._delay:
            time.sleep(self._delay - (time.time() - t0))
        
        # return chosen_bet
        raise NotImplementedError("You must implement the place_bet method, do not instantiate the TemplateBot class directly.")