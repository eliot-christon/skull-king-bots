__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.Card import Card
from src.model.cards.CardCollection import CardCollection
from .Graphics import Graphics
from ..model.Game import Game


class ConsoleGraphics(Graphics):
    """ConsoleGraphics class for the Skull King game"""

    def __init__(self) -> None:
        super().__init__()

    def render(self, game:Game) -> None:
        """Render the game in the console"""
        aff = "\n" * 10
        aff += f"Round:   {game.round}, state: {game.current_state}\n"
        aff += f"Trick:   {game.trick}\n"
        aff += f"{self.players_str(game)}\n"
        print(aff, flush=True, end="")

    def players_str(self, game:Game) -> str:
        """Render the players in the console"""
        spacing = [15, 5, 6]
        res = "Player name    |Score |Tricks |Hand\n------------------------------------\n"
        for player in game.players:
            for i, current_str in enumerate([player.name, str(player.score), f"{player.tricks} / {player.bet}"]):
                res += current_str + " " * (spacing[i] - len(current_str)) + "| "
            res += player.hand.__str__() + "\n"
        return res
    
    
    def get_number(self, min:int, max:int, text:str):
        """Get a number from the user"""
        choice = -1
        while choice < min or choice > max:
            try:
                choice = int(input(f"{text} (Between {min} and {max}): "))
            except ValueError:
                print("Please enter a valid number.")
                choice = -1
        return choice
    
    
    def choose_card(self, hand: CardCollection, playable_cards: CardCollection) -> Card:
        print("Choose a card to play.")
        print(playable_cards)
        choice = self.get_number(0, len(playable_cards)-1, "Enter the index of the card you want to play")
        return playable_cards[int(choice)]
    
    def place_bet(self, hand: CardCollection) -> int:
        print("Place a bet.")
        return self.get_number(0, len(hand), "Enter your bet")