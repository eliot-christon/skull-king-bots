__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .model.Game import Game
from .model.players.RandomPlayer import RandomPlayer
from .model.players.MiniMaxPlayer import MiniMaxPlayer
from .model.players.HumanPlayer import HumanPlayer
from .view.ConsoleGraphics import ConsoleGraphics
from .view.TkinterGraphics import TkinterGraphics
from .GameController import GameController


def main():
    """Main function"""
    
    graphics = TkinterGraphics()
    
    delay = 0.2
    player1 = RandomPlayer("Player 1", delay=delay)
    player2 = MiniMaxPlayer("Player 2", delay=delay)
    player3 = RandomPlayer("Player 3", delay=delay)
    player4 = RandomPlayer("Player 4", delay=delay)
    player5 = RandomPlayer("The best", delay=delay)

    game = Game([player1, player2, player3, player4, player5])

    controller = GameController(game, graphics)

    controller.run()


if __name__ == "__main__":
    main()