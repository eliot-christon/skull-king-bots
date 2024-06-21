__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .model.Game import Game
from .model.players.ComputerPlayer import ComputerPlayer
from .model.players.HumanPlayer import HumanPlayer
from .view.ConsoleGraphics import ConsoleGraphics
from .GameController import GameController


def main():
    """Main function"""
    delay = 0.2
    player1 = ComputerPlayer("Player 1", delay=delay)
    player2 = ComputerPlayer("Player 2", delay=delay)
    player3 = ComputerPlayer("Player 3", delay=delay)
    player4 = ComputerPlayer("Player 4", delay=delay)
    player5 = HumanPlayer("The best")

    game = Game([player1, player2, player3, player4, player5])

    graphics = ConsoleGraphics(game)

    controller = GameController(game, graphics)

    controller.run()


    

if __name__ == "__main__":
    main()