__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Card import Card
from .NumberCard import NumberCard, TrumpCard
from .CharacterCard import CharacterCard, Pirate, Mermaid, SkullKing, Flag, Tigress, Jack
from .AnimalCard import AnimalCard, Krakken, Whale, Plankton

from typing import List, Union


class CardCollection:
    """CardCollection class for the Skull King game. A collection of cards."""

    def __init__(self, cards:List[Card]) -> None:
        self.__cards = cards

    def __str__(self) -> str:
        str_card_list = ["( {} )" .format(card) for card in self.__cards]
        return f"{', '.join(str_card_list)}"
    
    def __len__(self) -> int:
        return len(self.__cards)
    
    def __iter__(self):
        return iter(self.__cards)
    
    def __getitem__(self, index: Union[int, slice]) -> Union[Card, 'CardCollection']:
        if isinstance(index, int):
            return self.__cards[index]
        elif isinstance(index, slice):
            return CardCollection(self.__cards[index])
        else:
            raise TypeError("Index must be an int or slice")
    
    def __setitem__(self, index:int, card:Card) -> None:
        self.__cards[index] = card
    
    def __add__(self, other:"CardCollection") -> "CardCollection":
        return CardCollection(self.__cards + other.__cards)
    
    def __iadd__(self, other:"CardCollection") -> "CardCollection":
        self.__cards += other.__cards
        return self
    
    def __sub__(self, other:"CardCollection") -> "CardCollection":
        return CardCollection([card for card in self.__cards if card not in other.__cards])
    
    def __isub__(self, other:"CardCollection") -> "CardCollection":
        self.__cards = [card for card in self.__cards if card not in other.__cards]
        return self
    
    def __eq__(self, other:"CardCollection") -> bool:
        return self.__cards == other.__cards

    def add(self, card:Card) -> None:
        """Add a card to the collection"""
        self.__cards.append(card)

    def remove(self, card:Card) -> None:
        """Remove a card from the collection"""
        self.__cards.remove(card)

    def shuffle(self) -> None:
        """Shuffle the collection"""
        import random
        random.shuffle(self.__cards)
    
    def clear(self) -> None:
        """Clear the collection"""
        self.__cards.clear()
    
    def copy(self) -> "CardCollection":
        """Return a copy of the collection"""
        copy = CardCollection()
        for card in self.__cards:
            copy.add(card)
        return copy
    

#%% GAME MECHANICS

    def requested_color(self) -> str:
        """Return the requested color of the trick"""

        for card in self.__cards:
            if isinstance(card, NumberCard):
                return card.color
            elif isinstance(card, CharacterCard) and card.value > 14:
                break
        return 'any'

    def first_index_of(self, card:Card) -> int:
        """Return the index of the first card in the collection"""
        return self.__cards.index(card)

    def highest_card(self) -> Card:
        """Return the highest card in the collection"""
        return max(self.__cards, key=lambda card: card.value)

    def lowest_card(self) -> Card:
        """Return the lowest card in the collection"""
        return min(self.__cards, key=lambda card: card.value)

    def last_type_card(self, card_type:type) -> Card:
        """Return the last card of a specific type"""
        for card in reversed(self.__cards):
            if isinstance(card, card_type):
                return card
        return None

    def first_type_card(self, card_type:type) -> Card:
        """Return the first card of a specific type"""
        for card in self.__cards:
            if isinstance(card, card_type):
                return card
        return None
    
    def cards_of_color(self, color:str) -> "CardCollection":
        """Return the cards of a specific color"""
        return CardCollection([card for card in self.__cards if card.color == color])

    def cards_of_type(self, card_type:type) -> "CardCollection":
        """Return the cards of a specific type"""
        return CardCollection([card for card in self.__cards if isinstance(card, card_type)])

    def bonus(self, winning_card:Card) -> int:
        """Return the bonus points for the trick.
        +10 for each 14-value card
        +10 for the 14-value trump card
        +20 for each Mermaid card if winning_card is Pirate
        +30 for each Pirate (value > 14) card if winning_card is SkullKing
        +40 for the SkullKing card if winning_card is Mermaid
        """
        bonus = 0
        for card in self.__cards:
            if card.value == 14:
                bonus += 10
            if isinstance(card, TrumpCard) and card.value == 14:
                bonus += 10
            elif isinstance(card, Mermaid) and isinstance(winning_card, Pirate):
                bonus += 20
            elif isinstance(card, Pirate) and card.value > 14 and isinstance(winning_card, SkullKing):
                bonus += 30
            elif isinstance(card, SkullKing) and isinstance(winning_card, Mermaid):
                bonus += 40
        return bonus

    def winning_card(self) -> Card:
        """Return the winning card"""
        # if no card in collection, return None
        if len(self.__cards) == 0:
            return None

        # if no AnimalCard is played
        if len(self.cards_of_type(AnimalCard)) == 0 or len(self.cards_of_type(Jack)) > 0:
            # if no CharacterCard (value > 14) is played
            if not any(card.value > 14 for card in self.__cards):
                # if no TrumpCard is played
                if len(self.cards_of_type(TrumpCard)) == 0:
                    # if no NumberCard is played => only Flag is played
                    if len(self.cards_of_type(NumberCard)) == 0:
                        return self.__cards[0] # return the first card
                    return self.cards_of_color(self.requested_color()).highest_card()
                return self.cards_of_type(TrumpCard).highest_card()
            # if SkullKing in the trick
            if len(self.cards_of_type(SkullKing)) > 0:
                # if Mermaid in the trick
                if len(self.cards_of_type(Mermaid)) > 0:
                    return Mermaid()
                return SkullKing()
            # elif Pirate in the trick
            elif any(isinstance(card, Pirate) for card in self.__cards if card.value > 14):
                return next(card for card in self.__cards if isinstance(card, Pirate) and card.value > 14)
            return Mermaid()
        
        # else: # if AnimalCard is played
        role = self.last_type_card(AnimalCard).__class__
        if role == Krakken:
            return None
        elif role == Plankton:
            return self.cards_of_type(NumberCard).lowest_card()
        elif role == Whale:
            return self.cards_of_type(NumberCard).highest_card()
        
        raise Exception("Exception in winning_card(), should not reach here")


def get_basic_deck() -> CardCollection:
    result = CardCollection([])
    for color in ['yellow', 'green', 'violet']:
        for value in range(1, 15):
            result.add(NumberCard(color, value))
    for value in range(1, 15):
        result.add(TrumpCard(value))
    
    for _ in range(5): result.add(Flag())
    for i in range(5): result.add(Pirate(i+1))
    for i in range(2): result.add(Mermaid(i+1))
    for _ in range(1): result.add(SkullKing())

    result.add(Jack())
    result.add(Tigress())

    result.add(Whale())
    result.add(Plankton())
    result.add(Krakken())

    return result




if __name__ == "__main__":
    print("This module is not meant to be run on its own.")