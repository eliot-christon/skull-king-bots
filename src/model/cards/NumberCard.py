__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Card import Card


class NumberCard(Card):
    """NumberCard class for the Skull King game"""

    def __init__(self, color:str, value:int) -> None:
        super().__init__(value=value, name=str(value) + " " + color, color=color)
    
    def __str__(self) -> str:
        return f"{self._name} of {self._color}"

    def details(self) -> str:
        return f"The {self._name} of {self._color}."


class TrumpCard(NumberCard):
    """TrumpCard class for the Skull King game"""

    def __init__(self, value:int) -> None:
        super().__init__(value=value, color="black")
    
    def details(self) -> str:
        return f"The {self._name} of {self._color} is a trump card."
