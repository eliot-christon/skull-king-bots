__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from ..cards.CardCollection import CardCollection
from ..cards.Card import Card
from ..cards.NumberCard import NumberCard


from abc import abstractmethod


class Player:
    """Abstract Player class for the Skull King game"""

    def __init__(self, name:str) -> None:
        self._name = name
        self._hand = CardCollection([])
        self._bet = 0
        self._tricks = 0
        self._bonus = 0
        self._score = 0
    
    def __str__(self) -> str:
        return f"Player: {self._name}, Score: {self._score}"
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def hand(self) -> CardCollection:
        return self._hand
    
    @property
    def score(self) -> int:
        return self._score

    @property
    def bet(self) -> int:
        return self._bet
    
    @property
    def tricks(self) -> int:
        return self._tricks
    
    @property
    def bonus(self) -> int:
        return self._bonus
    
    @bet.setter
    def bet(self, bet:int) -> None:
        self._bet = bet
    
    @tricks.setter
    def tricks(self, tricks:int) -> None:
        self._tricks = tricks
    
    @score.setter
    def score(self, score:int) -> None:
        self._score = score
    
    @hand.setter
    def hand(self, hand:CardCollection) -> None:
        self._hand = hand

    @bonus.setter
    def bonus(self, bonus:int) -> None:
        self._bonus = bonus
    
    def play_card(self, card:"Card") -> None:
        self._hand.remove(card)
    
    def details(self) -> str:
        return f"Player: {self._name}, Score: {self._score}, Bet: {self._bet}, Tricks: {self._tricks}, Bonus: {self._bonus}"
    
    def playable_cards(self, requested_color:str) -> CardCollection:
        """Return the cards that can be played"""
        if len(self._hand.cards_of_color(requested_color)) == 0:
            return self._hand
        return self._hand - self.hand.cards_of_type(NumberCard) + self._hand.cards_of_color(requested_color)

    @abstractmethod
    def choose_card(self, requested_color:str) -> "Card":
        pass

    @abstractmethod
    def place_bet(self) -> int:
        pass
    