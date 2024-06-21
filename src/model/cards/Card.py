__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from abc import ABC, abstractmethod


class Card(ABC):
    """Card abscract class for the Skull King game"""

    def __init__(self, value:int, name:str, color:str) -> None:
        self._value = value
        self._name = name
        self._color = color
    
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __eq__(self, other:"Card") -> bool:
        if not isinstance(other, Card):     return False
        if self._value != other.value:     return False
        if self._name != other.name:       return False
        if self._color != other.color:     return False
        return True
    
    @abstractmethod
    def details(self) -> str:
        pass

    @property
    def value(self) -> int:
        return self._value

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def color(self) -> str:
        return self._color
