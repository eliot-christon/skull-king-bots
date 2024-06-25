__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.Card import Card
from src.model.cards.CardCollection import CardCollection
from .Graphics import Graphics
from ..model.Game import Game

import pygame
from pygame_widgets.button import Button, ButtonArray
from typing import List, Dict, Tuple


class PygameGraphics(Graphics):

    def __init__(self):
        super().__init__()
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.card_assets = "assets/cards/"
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'bg': (0, 0, 0),
        }

#%% SCREENS

    def start_screen(self) -> None:
        self.screen.fill(self.colors['bg'])
        font = pygame.font.Font(None, 36)
        text = font.render("Welcome to Skull King!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, text_rect)
        # button
        self.start_button = Button(win=self.screen, x=self.width//2-50, y=self.height//2+50, width=100, height=50, text='Start', fontSize=20, margin=20, onClick=self.on_start_button_click)

    def bet_screen(self, hand:CardCollection) -> None:
        self.screen.fill(self.colors['bg'])
        font = pygame.font.Font(None, 36)
        text = font.render("Place a bet", True, self.colors['white'])
        text_rect = text.get_rect(center=(self.width//2, 50))
        self.screen.blit(text, text_rect)
        # cards
        self.display_cards(cards=hand, x_center=self.width//2, y_center=self.height//2, spacing=100, card_size=(100, 150))
        # buttons from 0 to len(hand)
        texts = [str(i) for i in range(len(hand)+1)]
        functions = [lambda i=i: self.on_bet_click(i) for i in range(len(hand)+1)]
        self.bet_buttons = ButtonArray(self.screen, x=self.width//2-50, y=self.height//2+100, width=100, height=50, texts=texts, fontSize=20, margin=20, onClicks=functions)

    def trick_screen(self, game:Game) -> None:
        self.screen.fill(self.colors['bg'])
        self.display_players(game.players, game.current_player, self.width//2, self.height//2, 100)
        # trick
        

    def play_screen(self, game:Game) -> None:
        pass

    def history_screen(self, history:List[Dict[str, Dict[str, int]]]) -> None:
        pass

#%% INTERACTIONS

    def choose_card_interaction(self, hand:CardCollection, playable_cards:CardCollection) -> Card:
        pass

    def place_bet(self, hand:CardCollection) -> int:
        pass
    
#%% EVENTS

    def on_card_click(self, event):
        pass

    def on_bet_click(self, number:int):
        pass
    
    def on_closing(self):
        pass
        
    def on_start_button_click(self):
        pass

#%% UTILS

    def display_card(self, card:Card, x_center:int, y_center:int, size:Tuple[int, int]) -> None:
        """Display a card"""
        card_img = pygame.image.load(f"{self.card_assets}{card}.png")
        card_img = pygame.transform.scale(card_img, size)
        self.screen.blit(card_img, (x_center - size[0]//2, y_center - size[1]//2))

    def display_cards(self, cards:CardCollection, x_center:int, y_center:int, spacing:int, card_size:Tuple[int, int]) -> None:
        """Display a hand of cards"""
        for i, card in enumerate(cards):
            self.display_card(card, x_center + i * spacing, y_center, card_size)
    
    def display_players(self, players:list, current_player, x_center:int, y_center:int, spacing:int) -> None:
        """Display the players"""
        for i, player in enumerate(players):
            display_str = f"{player.name} - {player.score} - {player.tricks}/{player.bet}"
            font = pygame.font.Font(None, 36)
            text = font.render(display_str, True, self.colors['white'])
            text_rect = text.get_rect(center=(x_center + i * spacing, y_center))
            self.screen.blit(text, text_rect)
            if player == current_player:
                pygame.draw.circle(self.screen, self.colors['red'], (x_center + i * spacing, y_center + 50), 10)