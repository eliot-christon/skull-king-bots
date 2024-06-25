__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .model.Game import Game
from .model.players.RandomPlayer import RandomPlayer
from .model.players.TrickCompletionBot import TrickCompletionBot
from .model.players.HumanPlayer import HumanPlayer
from .view.ConsoleGraphics import ConsoleGraphics
from .view.TkinterGraphics import TkinterGraphics
from .GameController import GameController


def main():
    """Main function"""
    
    graphics = TkinterGraphics()
    
    delay = 0.05
    player1 = RandomPlayer("Player 1", delay=delay)
    player2 = TrickCompletionBot("Player 2", delay=delay)
    player3 = RandomPlayer("Player 3", delay=delay)
    player4 = RandomPlayer("Player 4", delay=delay)
    player5 = HumanPlayer("The best", graphics=graphics)

    game = Game([player1, player2, player3, player4, player5], delays=False)

    controller = GameController(game, graphics)

    controller.run()


def main2():
    """Main function"""
        
    graphics = TkinterGraphics()
    
    delay = 0.05
    player1 = RandomPlayer("Random Bot 1", delay=delay)
    player2 = TrickCompletionBot("TC Bot 1", delay=delay)
    player3 = TrickCompletionBot("TC Bot 2", delay=delay)
    player4 = RandomPlayer("Random Bot 2", delay=delay)
    player5 = HumanPlayer("Human", graphics=graphics)

    game = Game([player1, player2, player3, player4, player5], delays=False)

    controller = GameController(game, graphics)

    controller.run()


if __name__ == "__main__":
    main2()