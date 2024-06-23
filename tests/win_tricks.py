__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.CardCollection import CardCollection, get_basic_deck
from src.model.cards.CharacterCard import Mermaid, Pirate, SkullKing, Flag, Tigress, Jack
from src.model.cards.NumberCard import NumberCard, TrumpCard
from src.model.cards.AnimalCard import Whale, Plankton, Krakken

if __name__ == "__main__":
    deck = get_basic_deck()
    
    #%% MERMAID TESTS
    
    trick = CardCollection([NumberCard("Red", 1), NumberCard("Red", 2), Jack(), SkullKing(), NumberCard("Red", 3), Mermaid(1), TrumpCard(14)])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Mermaid(1), f"Expected Mermaid(1), got {winning_card}"
    assert bonus == 60, f"Expected 60 bonus points got {bonus}"
    
    trick = CardCollection([NumberCard("Brown", 13), NumberCard("Red", 12), Pirate(3), SkullKing(), Mermaid(2)])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Mermaid(2), f"Expected Mermaid(2), got {winning_card}"
    assert bonus == 40, f"Expected 40 bonus points got {bonus}"
    
    trick = CardCollection([NumberCard("Brown", 13), NumberCard("Red", 12), Mermaid(2), TrumpCard(1), Flag()])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Mermaid(2), f"Expected Mermaid(2), got {winning_card}"
    assert bonus == 0, f"Expected 0 bonus points got {bonus}"
    
    #%% SKULLKING TESTS
    
    trick = CardCollection([NumberCard("Red", 1), NumberCard("Red", 2), Jack(), SkullKing(), NumberCard("Red", 3), Pirate(1), TrumpCard(13)])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == SkullKing(), f"Expected SkullKing(), got {winning_card}"
    assert bonus == 60, f"Expected 60 bonus points got {bonus}"
    
    #%% WHALE TESTS
    
    trick = CardCollection([NumberCard("Red", 1), NumberCard("Brown", 12), Pirate(4), SkullKing(), NumberCard("Red", 3), Whale(), TrumpCard(11)])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == NumberCard("Brown", 12), f"Expected NumberCard('Brown', 12), got {winning_card}"
    assert bonus == 0, f"Expected 0 bonus points got {bonus}"
    
    trick = CardCollection([Pirate(1), Pirate(4), Whale()])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Pirate(1), f"Expected Pirate(1), got {winning_card}"
    assert bonus == 0, f"Expected 0 bonus points got {bonus}"
    
    trick = CardCollection([Pirate(4), Pirate(1), Whale(), SkullKing()])
    winning_card = trick.winning_card()
    bonus = trick.bonus(trick.winning_card())
    assert winning_card == SkullKing(), f"Expected SkullKing(), got {winning_card}"
    assert bonus == 60, f"Expected 60 bonus points got {bonus}"
    
    
    #%% PLANKTON TESTS
    
    trick = CardCollection([NumberCard("Red", 14), NumberCard("Brown", 12), Pirate(4), SkullKing(), NumberCard("Purple", 3), Plankton(), TrumpCard(11)])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == NumberCard("Purple", 3), f"Expected NumberCard('Purple', 3), got {winning_card}"
    assert bonus == 10, f"Expected 10 bonus points got {bonus}"
    
    trick = CardCollection([Pirate(1), Pirate(4), Plankton()])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Pirate(1), f"Expected Pirate(1), got {winning_card}"
    assert bonus == 0, f"Expected 0 bonus points got {bonus}"
    
    trick = CardCollection([Whale(), Krakken(), Plankton()])
    winning_card = trick.winning_card()
    bonus = trick.bonus(winning_card)
    assert winning_card == Whale(), f"Expected Whale(), got {winning_card}"
    assert bonus == 0, f"Expected 0 bonus points got {bonus}"
    