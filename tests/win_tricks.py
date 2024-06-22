__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.CardCollection import CardCollection, get_basic_deck
from src.model.cards.CharacterCard import Mermaid, Pirate, SkullKing, Flag, Tigress, Jack
from src.model.cards.NumberCard import NumberCard, TrumpCard

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
    
    