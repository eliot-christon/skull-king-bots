__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Card import Card

from abc import abstractmethod


class CharacterCard(Card):
    """CharacterCard class for the Skull King game"""

    def __init__(self, value:int, name:str, color:str) -> None:
        super().__init__(value=value, name=name, color=color)
    
    def __str__(self) -> str:
        return f"{self._name}"
    
    @abstractmethod
    def details(self) -> str:
        pass


class Pirate(CharacterCard):
    """Pirate class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(value=16, name="Pirate", color="red")
    
    def details(self) -> str:
        return "The Pirate wins the trick, unless the Skull King is played or another Pirate is played before it."


class Jack(Pirate):
    """Jack class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__()
        self._name = "Jack"
    
    def details(self) -> str:
        return "Jack is a Pirate and cancels the effect of the Animal Cards played in the trick."
    

class Tigress(Pirate):
    """Tigress class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__()
        self._name = "Tigress"
    
    def as_flag(self) -> None:
        self._name = "Tigress Flag"
        self._value = 0
    
    def details(self) -> str:
        return "The Tigress can be played as a Pirate or as a flag."


class Mermaid(CharacterCard):
    """Mermaid class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(value=15, name="Mermaid", color="cyan")
    
    def details(self) -> str:
        return "The Mermaid wins the trick, unless a Pirate is played or another Mermaid is played before it."


class SkullKing(CharacterCard):
    """SkullKing class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(value=17, name="Skull King", color="black")
    
    def details(self) -> str:
        return "The Skull King wins the trick, unless a Mermaid is played."


class Flag(CharacterCard):
    """Flag class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__(value=0, name="Flag", color="white")
    
    def details(self) -> str:
        return "The Flag loses the trick. (Unless it's the first card played and only flags are played in the trick)"