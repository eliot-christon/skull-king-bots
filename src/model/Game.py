__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .players.Player import Player
from .cards.CardCollection import CardCollection, get_basic_deck
from .cards.AnimalCard import Krakken

from typing import List
from enum import Enum, auto


class GameState(Enum):
    """Enum for the game state"""
    START_ROUND = auto()
    DEAL = auto()
    BET = auto()
    START_TRICK = auto()
    PLAY_CARD = auto()
    END_TRICK = auto()
    END_ROUND = auto()
    END_GAME = auto()


class Game:
    """Game class for the Skull King game"""

    def __init__(self, players:List[Player]) -> None:
        self._players = players
        self._deck = get_basic_deck()
        self._round = 1
        self._trick = CardCollection([])
        self._last_winning_player = Player("Dummy1")
        self._current_player = Player("Dummy2")
        self._running = True

        self.current_state = GameState.START_ROUND

        self._transitions = {
            GameState.START_ROUND: {self.cond_true: GameState.DEAL},
            GameState.DEAL: {self.cond_true: GameState.BET},
            GameState.BET: {self.cond_true: GameState.START_TRICK},
            GameState.START_TRICK: {self.cond_true: GameState.PLAY_CARD},
            GameState.PLAY_CARD: {self.cond_all_players_played: GameState.END_TRICK, self.cond_else: GameState.PLAY_CARD},
            GameState.END_TRICK: {self.cond_round_ended: GameState.END_ROUND, self.cond_else: GameState.START_TRICK},
            GameState.END_ROUND: {self.cond_game_ended: GameState.END_GAME, self.cond_else: GameState.START_ROUND},
            GameState.END_GAME: {}
        }

        self._actions = {
            GameState.START_ROUND: self.start_round,
            GameState.DEAL: self.deal,
            GameState.BET: self.place_bets,
            GameState.START_TRICK: self.start_trick,
            GameState.PLAY_CARD: self.play_card,
            GameState.END_TRICK: self.end_trick,
            GameState.END_ROUND: self.end_round,
            GameState.END_GAME: self.end_game
        }

    def __str__(self) -> str:
        return f"Game: Players: {self._players}, Round: {self._round}"

#%% PROPERTIES =======================================================================================

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def deck(self) -> CardCollection:
        return self._deck

    @property
    def round(self) -> int:
        return self._round
    
    @property
    def trick(self) -> CardCollection:
        return self._trick
    
    @property
    def running(self) -> bool:
        return self._running

#%% CONDITIONS ======================================================================================

    def cond_true(self) -> bool:
        return True
    
    def cond_else(self) -> bool:
        return True
    
    def cond_all_players_played(self) -> bool:
        """Check if all players have played their card"""
        return len(self._trick) == len(self._players)
    
    def cond_round_ended(self) -> bool:
        """Check if the round has ended by checking the number of cards in the players' hands"""
        return all(len(player.hand) == 0 for player in self._players)

    def cond_game_ended(self) -> bool:
        """Check if the game has ended by checking the number of rounds"""
        return self.round == 10

#%% ACTIONS =========================================================================================

    def start_round(self) -> None:
        """Start a round of the game"""
        self._players = self.roll_players()
        self._trick = CardCollection([])
        for player in self._players:
            player.bet = 0
            player.tricks = 0
            player.bonus = 0
        self._last_winning_player = self._players[0] # Start the round with the first player

    def deal(self) -> None:
        """Deal cards to the players"""
        # Shuffle the deck
        self._deck.shuffle()
        for i, player in enumerate(self._players):
            player.hand = self._deck[i*self.round:(i+1)*self.round]

    def place_bets(self) -> None:
        """Have each player place a bet"""
        for player in self._players:
            bet = player.place_bet()
            player.bet = bet
        
    def start_trick(self) -> None:
        """Start a trick"""
        self._trick = CardCollection([])
        self._current_player = self._last_winning_player # Start the trick with the winner of the last trick

    def play_card(self) -> None:
        """Have the current player play a card"""
        chosen_card = self._current_player.choose_card(requested_color=self._trick.requested_color())
        self._trick.add(chosen_card)
        self._current_player.play_card(chosen_card)
        self._current_player = self._players[(self._players.index(self._current_player) + 1) % len(self._players)]
    
    def end_trick(self) -> None:
        """End a trick, calculate the winner and give the points"""
        winning_card = self._trick.winning_card()
        if winning_card is None:
            # search for the Krakken card, the player next to it will start the next trick
            self._last_winning_player = self._players[(self._trick.first_index_of(Krakken()) + 1) % len(self._players)]
        else:
            bonus = self._trick.bonus(winning_card)
            self._last_winning_player = self._players[self._trick.first_index_of(winning_card)]
            self._last_winning_player.tricks += 1
            self._last_winning_player.bonus += bonus
    
    def end_round(self) -> None:
        """End a round, calculate the scores"""
        self.calculate_scores()
        self._round += 1

    def end_game(self) -> None:
        """End the game"""
        self._running = False

#%% UTILS ============================================================================================

    def roll_players(self, offset:int=1) -> List[Player]:
        """Roll the players by the offset"""
        return self._players[offset:] + self._players[:offset]
    
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
    
#%% GAME LOOP ========================================================================================

    def game_step(self) -> None:
        """A step of the game"""
        self._actions[self.current_state]()
        next_state = None
        if self.cond_else in self._transitions[self.current_state]:
            next_state = self._transitions[self.current_state][self.cond_else]

        for condition in self._transitions[self.current_state]:
            if condition() and condition != self.cond_else:
                next_state = self._transitions[self.current_state][condition]
                break
        
        self.current_state = next_state