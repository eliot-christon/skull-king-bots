__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .players.Player import Player
from .cards.CardCollection import CardCollection, get_basic_deck

from typing import List


class Game:
    """Game class for the Skull King game"""

    def __init__(self, players:List[Player]) -> None:
        self._players = players
        self._deck = get_basic_deck()
        self._round = 1
        self._current_player_index = 0

    def __str__(self) -> str:
        return f"Game: Players: {self._players}, Round: {self._round}"

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def deck(self) -> CardCollection:
        return self._deck

    @property
    def round(self) -> int:
        return self._round
    
    @round.setter # TODO: delete this setter
    def round(self, round:int) -> None:
        self._round = round
    
    def roll_players(self, offset:int=1) -> List[Player]:
        """Roll the players by the offset"""
        return self._players[offset:] + self._players[:offset]

    def deal(self) -> None:
        """Deal cards to the players"""
        # Shuffle the deck
        self._deck.shuffle()
        for i, player in enumerate(self._players):
            player.hand = self._deck[i*self.round:(i+1)*self.round]
            player.bet = 0
            player.tricks = 0
            player.bonus = 0
    
    def play_bets(self) -> None:
        """Have each player place a bet"""
        for player in self._players:
            bet = player.place_bet()
            player.bet = bet

    def play_trick(self) -> None:
        """Play a trick"""
        trick = CardCollection([])
        players = self.roll_players(offset=self._current_player_index)
        for player in players:
            chosen_card = player.choose_card(requested_color=trick.requested_color())
            trick.add(chosen_card)
            player.play_card(chosen_card)
        # Determine the winner of the trick
        winning_card = trick.winning_card()
        if winning_card is None:
            return
        bonus = trick.bonus(winning_card)
        self._current_player_index = trick.first_index_of(winning_card)
        win_trick_player = players[self._current_player_index]
        win_trick_player.tricks += 1
        win_trick_player.bonus += bonus

    def calculate_scores(self) -> None:
        """Calculate the scores for each player"""
        for player in self._players:
            if player.bet == 0:
                if player.tricks == 0:
                    player.score += 10*self.round + player.bonus
                else:
                    player.score -= 10*self.round
            else:
                if player.tricks == player.bet:
                    player.score += 20*player.tricks + player.bonus
                else:
                    player.score -= 10*abs(player.tricks - player.bet)

    def play_round(self) -> None:
        """Play a round of the game"""
        self._current_player_index = 0
        self.deal()
        self.play_bets()
        for _ in range(self.round):
            self.play_trick()
        self.calculate_scores()
        self._round += 1
        self._players = self.roll_players()

    def play_game(self) -> None:
        """Play the game"""
        while self.round < 10:
            self.play_round()