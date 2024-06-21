__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Graphics import Graphics
from ..model.Game import Game

import os


class ConsoleGraphics(Graphics):
    """ConsoleGraphics class for the Skull King game"""

    def __init__(self, game:Game) -> None:
        super().__init__(game=game)

    def render(self) -> None:
        """Render the game in the console"""
        aff = "\n" * 10
        aff += f"Round:   {self._game.round}, state: {self._game.current_state}\n"
        aff += f"Trick:   {self._game.trick}\n"
        aff += f"{self.players_str()}\n"
        print(aff, flush=True, end="")

    def players_str(self) -> str:
        """Render the players in the console"""
        spacing = [15, 5, 6]
        res = "Player name    |Score |Tricks |Hand\n------------------------------------\n"
        for player in self._game.players:
            for i, current_str in enumerate([player.name, str(player.score), f"{player.tricks} / {player.bet}"]):
                res += current_str + " " * (spacing[i] - len(current_str)) + "| "
            res += player.hand.__str__() + "\n"
        return res