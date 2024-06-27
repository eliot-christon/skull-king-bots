__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .ComputerPlayer import ComputerPlayer
from ..cards.Card import Card
from ..cards.CharacterCard import CharacterCard
from ..cards.NumberCard import TrumpCard
from ..cards.CardCollection import CardCollection, get_basic_deck

import random
import time
from typing import Dict, Any
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Dense


class GeneticBot(ComputerPlayer):
    """GeneticBot class for the Skull King game, a bot trained using genetic algorithms"""

    def __init__(self, name:str, delay:float=0.1, deck:CardCollection=get_basic_deck()) -> None:
        super().__init__(name=name, delay=delay)

        self.card_colors = np.array([card.color for card in deck])
        self.u_card_colors = np.unique(self.card_colors)
        self.count_card_colors = {card_color: np.sum(self.card_colors == card_color) for card_color in self.u_card_colors}
        self.card_values = np.array([card.value for card in deck])
        self.u_card_values = np.unique(self.card_values)
        self.count_card_values = {card_value: np.sum(self.card_values == card_value) for card_value in self.u_card_values}
        self.card_types = np.array([type(card) for card in deck])
        self.u_card_types = np.array(list(set(self.card_types)))
        self.count_card_types = {card_type: np.sum(self.card_types == card_type) for card_type in self.u_card_types}

        self._model = self.blank_model()

    def blank_model(self) -> "Model":
        """Create a model for the bot to use"""
        model = Sequential()
        model.add(Dense(64, input_shape=(115,), activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
    
    @property
    def model(self) -> "Model":
        """Get the model for the bot to use"""
        return self._model

    def set_model(self, model:Model) -> None:
        """Set the model for the bot to use"""
        self._model = model
    
    def choose_card(self, features:Dict[str, Any]) -> "Card":
        t0 = time.time() # to keep track of the time taken by the bot to choose a card
        
        playable_cards = self.playable_cards(features["trick"].requested_color()) # this method is essential to get the playable cards
        
        # extract features
        general_features = self.transform_features(features)

        if len(playable_cards) > 1:
            best_card = None
            best_score = -np.inf

            for card in playable_cards:
                card_features = self.card_features(card, features["trick"])
                total_features = np.concatenate([general_features, card_features]).reshape(1, -1)
                score = self._model.predict(total_features)
                if score > best_score:
                    best_score = score
                    best_card = card
        else:
            best_card = playable_cards[0]
        # delay just before returning the card
        if time.time() - t0 < self._delay:
            time.sleep(self._delay - (time.time() - t0))
        
        return best_card
    
    def place_bet(self) -> int:
        t0 = time.time() # to keep track of the time taken by the bot to place a bet
        
        # count the number of character cards in the hand and trump cards > 12
        n = len([card for card in self._hand if isinstance(card, CharacterCard) or (isinstance(card, TrumpCard) and card.value > 12)])
        chosen_bet = int(0.7 * n + 0.12 * len(self._hand))
        
        # delay just before returning the card
        if time.time() - t0 < self._delay:
            time.sleep(self._delay - (time.time() - t0))
        
        return chosen_bet
    
    def card_features(self, card:Card, trick:CardCollection) -> Dict[str, Any]:
        """Extract features from the card that can be used to make decisions"""
        value = card.value / max(self.u_card_values)
        max_value_same_color_in_trick = np.max([c.value for c in trick if c.color == card.color] + [0]) / max(self.u_card_values)
        min_value_same_color_in_trick = np.min([c.value for c in trick if c.color == card.color] + [max(self.u_card_values)]) / max(self.u_card_values)
        color = np.zeros(len(self.u_card_colors))
        color[np.where(self.u_card_colors == card.color)[0][0]] = 1
        card_type = np.zeros(len(self.u_card_types))
        card_type[np.where(self.u_card_types == type(card))[0][0]] = 1
        trick_ag = trick.copy() + CardCollection([card])
        would_win = 1 if card == trick_ag.winning_card() else 0
        return np.concatenate([np.array([value, max_value_same_color_in_trick, min_value_same_color_in_trick, would_win]), color, card_type])
    
    def transform_features(self, features:Dict[str, Any]) -> Dict[str, Any]:
        """Transform the features to a format that can be used by the bot to make decisions"""
        # features will now be a flat numpy array
        """
        features = {
            "round": round,
            "trick": trick,
            "players": players,
            "current_player": current_player,
            "round_history": round_history,
            "deck": deck
        }
        """
        MAX_PLAYERS = 7
        round_float = np.array([features["round"]/10])
        cards_after = np.array([(len(features["players"]) - len(features["trick"])) / len(features["players"])])

        players_bets = np.array([player.bet/features["round"] for player in features["players"]])
        players_bets = np.concatenate([players_bets, np.zeros(MAX_PLAYERS - len(players_bets))])
        players_tricks = np.array([player.tricks/features["round"] for player in features["players"]])
        players_tricks = np.concatenate([players_tricks, np.zeros(MAX_PLAYERS - len(players_tricks))])

        trick_values_count = np.zeros(len(self.u_card_values))
        trick_colors_count = np.zeros(len(self.u_card_colors))
        trick_types_count = np.zeros(len(self.u_card_types))
        for card in features["trick"]:
            trick_values_count[np.where(self.u_card_values == card.value)[0][0]] += 1/len(features["players"])
            trick_colors_count[np.where(self.u_card_colors == card.color)[0][0]] += 1/len(features["players"])
            trick_types_count[ np.where(self.u_card_types  == type(card))[0][0]] += 1/len(features["players"])
        trick_max_value = np.array([np.argmax(trick_values_count)])
        trick_min_value = np.array([np.argmin(trick_values_count)])

        round_history_values_count = np.zeros(len(self.u_card_values))
        round_history_colors_count = np.zeros(len(self.u_card_colors))
        round_history_types_count = np.zeros(len(self.u_card_types))
        for card in features["round_history"]:
            round_history_values_count[np.where(self.u_card_values == card.value)[0][0]] += 1/self.count_card_values[card.value]
            round_history_colors_count[np.where(self.u_card_colors == card.color)[0][0]] += 1/self.count_card_colors[card.color]
            round_history_types_count[ np.where(self.u_card_types  == type(card))[0][0]] += 1/self.count_card_types[type(card)]
        
        return np.concatenate([round_float, cards_after, trick_values_count, trick_colors_count, trick_types_count, round_history_values_count, round_history_colors_count, round_history_types_count, trick_max_value, trick_min_value, players_bets, players_tricks])



