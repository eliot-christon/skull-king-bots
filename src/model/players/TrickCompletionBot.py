__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from .Player import Player
from ..cards.Card import Card
from ..cards.CharacterCard import CharacterCard, Tigress
from ..cards.NumberCard import NumberCard, TrumpCard
from ..cards.CardCollection import CardCollection

from typing import Dict, Any, List
import time


class TrickCompletionBot(ComputerPlayer):
    """TrickCompletionBot class for the Skull King game, simulates a player that plays with a TrickCompletionBot strategy."""

    def __init__(self, name:str, delay:float=0.1) -> None:
        super().__init__(name=name, delay=delay)
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        """Chooses the best card to play using the MiniMax algorithm"""
        t0 = time.time()
        possible_cards = self.playable_cards(features["trick"].requested_color()).copy()
        if any(isinstance(card, Tigress) for card in possible_cards):
            possible_cards.add(Tigress().as_flag())
        current_trick = features["trick"]
        cards_not_played = features["deck"] - features["round_history"]
        players = features["players"]
        round = features["round"]
        
        best_score = -float("inf")
        best_card = possible_cards[0]
        
        if len(possible_cards) > 2:
            for card in possible_cards:
                possible_tricks = self.__create_all_possible_tricks(card, cards_not_played, current_trick, len(features["players"]))
                score = 0
                for trick in possible_tricks:
                    score += self.__evaluate_trick(trick, players, round)
                if score > best_score:
                    best_score = score
                    best_card = card
        
        if best_card == Tigress().as_flag():
            tigress_card_in_hand = [card for card in self._hand if isinstance(card, Tigress)][0]
            tigress_card_in_hand.as_flag()
            best_card = tigress_card_in_hand
        
        # delay
        if time.time() - t0 < self._delay:
            time.sleep(self._delay - (time.time() - t0))
        
        return best_card
    
    def place_bet(self) -> int:
        """Places the bet randomly"""
        # count the number of character cards in the hand and trump cards > 12
        n = len([card for card in self._hand if isinstance(card, CharacterCard) or (isinstance(card, TrumpCard) and card.value > 12)])
        return int(0.7 * n + 0.12 * len(self._hand))
    
    def __create_all_possible_tricks(self, chosen_card:Card, cards_not_played:CardCollection, current_trick:CardCollection, in_len_trick:int) -> List[CardCollection]:
        """Creates the game tree for the MiniMax algorithm with all the possible endings of the trick.
        Only next card played is the one of the player (possible_cards)"""
        possible_tricks = []
        len_trick = min(in_len_trick, len(current_trick) + 3)
        
        # recursive function
        def create_trick_tree(trick:CardCollection, cards_not_played:CardCollection, current_trick:CardCollection, len_trick:int) -> None:
            if len(trick) == len_trick:
                possible_tricks.append(trick)
                return
            for card in cards_not_played:
                trick_copy = trick.copy()
                trick_copy.add(card)
                create_trick_tree(trick_copy, cards_not_played.copy() - CardCollection([card]), current_trick, len_trick)
        
        trick = current_trick + CardCollection([chosen_card])
        create_trick_tree(trick, cards_not_played, current_trick, len_trick)
        
        return possible_tricks
    
    def __evaluate_trick(self, trick:CardCollection, players:List[Player], round:int) -> int:
        """Evaluates the trick and returns the score of the trick,
        the best score should favor the realisation of the player's bet with bonus points and the other players' failure"""
        winning_card = trick.winning_card()
        winning_player = players[trick.first_index_of(winning_card)] if winning_card else None
        bonus = trick.bonus(winning_card)
        tricks_to_win = self.bet - self.tricks
        
        if self == winning_player:
            if self.bet == 0:
                return -10 * round
            return (tricks_to_win - 1) * 10 + bonus * min(1, max(0, tricks_to_win - 1))
        else:
            winning_player_tricks_to_win = winning_player.bet - winning_player.tricks if winning_player else 0
            if self.bet == 0:
                return 10 * round
            return -10 * abs(tricks_to_win) - bonus * min(1, max(0, winning_player_tricks_to_win - 1)) - (winning_player_tricks_to_win - 1) * 10
    