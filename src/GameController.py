__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .model.Game import Game
from .view.Graphics import Graphics


class GameController:
    """GameController class for the Skull King game"""

    def __init__(self, game:Game, graphics:Graphics) -> None:
        self.__game     = game
        self.__graphics = graphics
    
    def run(self) -> None:
        """Play the game"""
        while self.__game.running and self.__graphics.running:
            try:
                self.__graphics.render(self.__game)
                self.__game.game_step()
            except KeyboardInterrupt:
                break
