__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Card import Card

from abc import abstractmethod


class AnimalCard(Card):
    """AnimalCard class for the Skull King game"""

    def __init__(self, name:str) -> None:
        super().__init__(value=0, name=name, color="grey")
    
    def __str__(self) -> str:
        return f"The {self._name}!"

    @abstractmethod
    def details(self) -> str:
        pass


class Whale(AnimalCard):
    """Whale class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(name="Whale")
    
    def details(self) -> str:
        return "The Whale cancels the effect of all character cards played in the trick. The highest number card wins the trick."


class Plankton(AnimalCard):
    """Plankton class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(name="Plankton")
    
    def details(self) -> str:
        return "The Plankton cancels the effect of all character cards played in the trick. The lowest number card wins the trick."


class Krakken(AnimalCard):
    """Krakken class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(name="Krakken")
    
    def details(self) -> str:
        return "The Krakken takes the trick, regardless of the cards played."