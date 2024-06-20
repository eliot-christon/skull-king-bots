__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .game.Game import Game
from .game.players.ComputerPlayer import ComputerPlayer


def main():
    """Main function"""
    player1 = ComputerPlayer("Player 1")
    player2 = ComputerPlayer("Player 2")
    player3 = ComputerPlayer("Player 3")
    player4 = ComputerPlayer("Player 4")
    game = Game([player1, player2, player3, player4])

    def print_players():
        for player in game.players:
            if len(player.hand) == 0:
                print('   ', end='')
                print(player.details())
            else:
                print('      ', end='')
                print(player.hand)

    for i in range(10):
        print(f"\nRound {i+1}")
        print('='*20)
        game.deal()
        game.play_bets()
        print_players()
        for _ in range(game.round - 1):
            game.play_trick()
            print('   -------------------')
            print_players()
        game.play_trick()
        game.calculate_scores()
        print('   -------------------')
        print_players()
        game.round += 1

if __name__ == "__main__":
    main()