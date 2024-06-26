__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'


from .Graphics import Graphics
from ..model.Game import Game
from ..model.cards.Card import Card
from ..model.cards.CardCollection import CardCollection

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from typing import List, Dict, Tuple


class PygameGraphics(Graphics):

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 900))
        self.card_assets = "assets/cards/"
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 155, 0),
            'blue': (0, 0, 255),
            'bg': (80, 80, 80),
        }
        self.card_sizes = {
            'original': (350, 500),
            'small': (100, 150),
        }
        self.clicked_start = False
        self.playable_cards_rects:List[pygame.Rect] = []

    @property
    def height(self) -> int:
        return self.screen.get_height()
    
    @property
    def width(self) -> int:
        return self.screen.get_width()

#%% ENTRY POINTS

    def start_screen(self) -> None:
        """display the start screen"""
        self.get_start_button()
        start_surf = self.start_surface()
        self.screen.blit(start_surf, (0, 0))

        pygame.display.update()
        while not self.clicked_start:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.on_closing()
            
            pygame_widgets.update(events)
            pygame.display.update()
        del self.start_button

    def render(self, game: Game) -> None:
        """Render the game"""
        self.screen.fill(self.colors['bg'])
        # Banner
        banner = self.banner_surface()
        self.screen.blit(banner, (0, 0))
        # Players
        player_surf = self.player_surface(game.players, game.current_player)
        self.screen.blit(player_surf, (0, self.height//10))
        # Round
        round_surf = self.round_surface(game.round)
        self.screen.blit(round_surf, (self.width//6, self.height//10))
        # Trick
        trick_surf = self.trick_surface(game.trick, max_cards=len(game.players))
        x_center = (7*self.width)//12
        y_top = (2.2*self.height)//10
        self.screen.blit(trick_surf, (x_center - trick_surf.get_width()//2, y_top))
        # Update the display
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.on_closing()
        
        pygame.display.update()

    def display_history(self, history: List[Dict[str, Dict[str, int]]]) -> None:
        # clear the screen
        self.screen.fill(self.colors['bg'])
        
        num_col = len(history[0]) + 1 # first column is the round number
        num_sub_col = 3 # for each player, score, tricks, bet
        num_row = len(history) + 2 # first two rows are the headers

        font = pygame.font.Font(None, self.height//40)
        small_font = pygame.font.Font(None, self.height//50)

        player_names = list(history[0].keys())

        x_min, x_max = self.width//10, (9*self.width)//10
        y_min, y_max = self.height//10, (9*self.height)//10
        x_step = (x_max - x_min) // num_col
        x_sub_step = x_step // num_sub_col
        y_step = (y_max - y_min) // num_row

        # headers
        for i, player_name in enumerate(["Round"] + player_names):
            text = font.render(player_name, True, self.colors['white'])
            text_rect = text.get_rect(center=(x_min + i*x_step + x_step//2, y_min + y_step//4))
            self.screen.blit(text, text_rect)
            # header 2 (for each player, score, tricks/bet, bonus)
            if i > 0:
                for j, sub_header in enumerate(["Score", "Tricks/Bet", "Bonus"]):
                    text = small_font.render(sub_header, True, self.colors['white'])
                    text_rect = text.get_rect(center=(x_min + i*x_step + j*x_sub_step + x_sub_step//2, y_min + (3*y_step)//4))
                    self.screen.blit(text, text_rect)
        
        # data
        for i, round_data in enumerate(history):
            for j, player_name in enumerate(["Round"] + player_names):
                if j == 0:
                    text = font.render(str(i+1), True, self.colors['white'])
                    text_rect = text.get_rect(center=(x_min + j*x_step + x_step//2, y_min + (i+1)*y_step + y_step//2))
                    self.screen.blit(text, text_rect)
                else:
                    # strings
                    score = str(round_data[player_name]["score"])
                    tricks_bet = f"{round_data[player_name]['tricks']}/{round_data[player_name]['bet']}"
                    bonus = f"+{round_data[player_name]['bonus']}" if round_data[player_name]['bonus'] > 0 else ""
                    # render
                    text = font.render(score, True, self.colors['white'])
                    text_rect = text.get_rect(center=(x_min + j*x_step + x_sub_step//2, y_min + (i+1)*y_step + y_step//2))
                    self.screen.blit(text, text_rect)
                    text = small_font.render(tricks_bet, True, self.colors['white'])
                    text_rect = text.get_rect(center=(x_min + j*x_step + x_sub_step + x_sub_step//2, y_min + (i+1)*y_step + y_step//2))
                    self.screen.blit(text, text_rect)
                    text = small_font.render(bonus, True, self.colors['white'])
                    text_rect = text.get_rect(center=(x_min + j*x_step + 2*x_sub_step + x_sub_step//2, y_min + (i+1)*y_step + y_step//2))
                    self.screen.blit(text, text_rect)

        winner_index = max(range(len(player_names)), key=lambda i: history[-1][player_names[i]]["score"])
        crown_icon = pygame.image.load("assets/icons/crown.png")
        crown_icon = pygame.transform.scale(crown_icon, (crown_icon.get_width()//4, crown_icon.get_height()//4))
        x_crown = x_min + (winner_index + 1)*x_step + x_step//2
        y_crown = y_min + (len(history)+1)*y_step + y_step//2
        self.screen.blit(crown_icon, (x_crown - crown_icon.get_width()//2, y_crown - crown_icon.get_height()//2))

        # draw lines
        for i in range(num_row):
            pygame.draw.line(self.screen, self.colors['white'], (x_min, y_min + i*y_step), (x_max, y_min + i*y_step), 2)
        for i in range(num_col + 1):
            pygame.draw.line(self.screen, self.colors['white'], (x_min + i*x_step, y_min), (x_min + i*x_step, y_max - y_step), 2)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.on_closing()
            pygame.display.update()

#%% INTERACTIONS

    def choose_card_interaction(self, hand:CardCollection, playable_cards:CardCollection) -> Card:
        """Let the player choose a card within the playable cards"""
        # Display the hand
        hand_surf = self.hand_surface(hand, playable_cards)
        hand_surf_size = hand_surf.get_size()
        hand_surf_pos = (self.width - hand_surf_size[0], self.height - hand_surf_size[1])
        self.screen.blit(hand_surf, hand_surf_pos)
        
        # update all playable cards rects by augmenting their position by the hand_surf position
        self.playable_cards_rects = [rect.move(hand_surf_pos) for rect in self.playable_cards_rects]


        chosen_card = None
        # Wait for the player to choose a card
        while chosen_card is None:
            # Update the display
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.on_closing()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for i, rect in enumerate(self.playable_cards_rects):
                        if rect.collidepoint(pos):
                            chosen_card = playable_cards[i]
                            break

            pygame.display.update()
        
        return chosen_card

    def place_bet(self, hand:CardCollection) -> int:
        """Let the player place a bet"""
        # Display the hand
        hand_surf = self.hand_surface(CardCollection(), hand)
        hand_surf_size = hand_surf.get_size()
        hand_surf_pos = (self.width - hand_surf_size[0], self.height - hand_surf_size[1])
        self.screen.blit(hand_surf, hand_surf_pos)

        # Display the bet surface just above the hand
        self.get_bet_slider(hand)
        self.get_bet_button()
        x_margin = self.width//40
        y_margin = self.height//60
        self.bet = None
        # Wait for the player to bet
        while self.bet is None:
            # Update the display
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.on_closing()
            
            self.screen.fill(self.colors["bg"], (self.bet_slider.getX() - x_margin, self.bet_slider.getY() - y_margin, self.bet_slider.getWidth() + 2*x_margin, self.bet_slider.getHeight() + 2*y_margin))
            self.bet_button.setText("Bet " + str(self.bet_slider.getValue()))
            pygame_widgets.update(events)
            pygame.display.update()
        
        del self.bet_slider
        del self.bet_button

        return self.bet

#%% SURFACES

    def banner_surface(self) -> pygame.Surface:
        """Create the banner surface"""
        banner = pygame.Surface((self.width, self.height//10))
        banner.fill(self.colors['bg'])
        banner_surf = pygame.image.load("assets/skullking_letters.png")
        heigth = banner.get_height()
        width = int(heigth * (banner_surf.get_width()/banner_surf.get_height()))
        banner_surf = pygame.transform.scale(banner_surf, (width, heigth))
        banner.blit(banner_surf, (self.width//2 - width//2, 0))
        return banner
    
    def player_surface(self, players, current_player) -> pygame.Surface:
        """Create the player surface"""
        player_surf = pygame.Surface((self.width//6, (9*self.height)//10))
        width, height = player_surf.get_size()
        player_surf.fill(self.colors['bg'])
        # Test PLAYER, Centered at the top
        # Then each player, with their name, score, tricks, and bet Like this: "bold_name\n score - tricks/bet" With bold player name bigger than the rest
        above_font = pygame.font.Font(None, self.height//20)
        above_text = above_font.render("Players", True, self.colors['white'])
        above_text_rect = above_text.get_rect(center=(width//2, height//20))
        player_surf.blit(above_text, above_text_rect)

        # horizontal line
        pygame.draw.line(player_surf, self.colors['white'], (0, height//12), (width, height//12), 2)

        font_player_name = pygame.font.Font(None, self.height//25)
        font_player_info = pygame.font.Font(None, self.height//28)

        for i, player in enumerate(players):
            if player == current_player:
                player_surf.fill(self.colors['green'], (0, (i + 1) * height//10, width, height//10))
            name = font_player_name.render(player.name, True, self.colors['white'])
            name_rect = name.get_rect(topleft=(width//8, (i + 1) * height//10))
            player_surf.blit(name, name_rect)
            bonus_str = f"+{player.bonus}" if player.bonus > 0 else ""
            info = font_player_info.render(f"{player.score} ({player.tricks}/{player.bet}) {bonus_str}", True, self.colors['white'])
            info_rect = info.get_rect(topleft=(width//5, (i + 1) * height//10 + height//20))
            player_surf.blit(info, info_rect)
        
        return player_surf
    
    def round_surface(self, round_number:int) -> pygame.Surface:
        """Create the round surface"""
        round_surf = pygame.Surface((self.width//6, self.height//10))
        width, height = round_surf.get_size()
        round_surf.fill(self.colors['bg'])
        # Round number
        font = pygame.font.Font(None, 24)
        text = font.render(f"Round {round_number}", True, self.colors['white'])
        text_rect = text.get_rect(center=(width//2, height//2))
        round_surf.blit(text, text_rect)
        return round_surf
    
    def trick_surface(self, trick:CardCollection, max_cards:int) -> pygame.Surface:
        return self.cards_surface((5*self.width)//7, trick, max_cards=max_cards, spacing_div=60, bg_color=self.colors['white'], max_height=(4*self.height)//10)
    
    def hand_surface(self, hand:CardCollection, playable_cards:CardCollection) -> pygame.Surface:
        return self.cards_surface((5*self.width)//6, playable_cards, dark_cards=hand-playable_cards, max_cards=10, spacing_div=200)
    
    def cards_surface(self,
                      width:int,
                      light_cards:CardCollection,
                      dark_cards:CardCollection=CardCollection(),
                      max_cards:int=10,
                      spacing_div:int=50,
                      bg_color:Tuple[int]=None,
                      max_height:int=None
                      ) -> pygame.Surface:
        """Create the a surface with the cards"""
        if bg_color is None:
            bg_color = self.colors["bg"]
        if max_height is None:
            max_height = self.height

        separator_spacing = width//spacing_div
        card_width = ( width - ( (max_cards + 1) * separator_spacing ) ) // max_cards # max_cards cards + max_cards separators
        card_height = int(card_width * (self.card_sizes['original'][1]/self.card_sizes['original'][0]))
        height = card_height + 2*separator_spacing

        if height > max_height:
            separator_spacing = max_height//spacing_div
            height = max_height
            card_height = height - 2*separator_spacing
            card_width = int(card_height * (self.card_sizes['original'][0]/self.card_sizes['original'][1]))
            width = card_width * max_cards + (max_cards + 1) * separator_spacing


        hand_surf = pygame.Surface((width, height))
        hand_surf.fill(bg_color)
        # Display the cards

        self.playable_cards_rects = []

        for i, card in enumerate(light_cards + dark_cards):
            card_surf = pygame.image.load(self.card_assets + card.name + ".png")
            card_surf = pygame.transform.scale(card_surf, (card_width, card_height))
            coords_top_left = (i*(card_width + separator_spacing) + separator_spacing, separator_spacing)
            if card in dark_cards:
                # make the image half transparent
                card_surf.set_alpha(128)
            else:
                self.playable_cards_rects.append(card_surf.get_rect(topleft=coords_top_left))
            
            hand_surf.blit(card_surf, coords_top_left)
        
        return hand_surf

    def start_surface(self) -> pygame.Surface:
        """Create the start surface"""
        start_surf = pygame.Surface((self.width, self.height))
        start_surf.fill(self.colors['bg'])
        # add start background
        start_bg = pygame.image.load("assets/background/start2.jpg")
        # transparence
        start_bg.set_alpha(200)
        start_surf.blit(start_bg, (self.width//2 - start_bg.get_width()//2, self.height//2 - start_bg.get_height()//2))
        # Add skullking letters
        skullking_surf = pygame.image.load("assets/skullking_letters.png")

        start_surf.blit(skullking_surf, (self.width//2 - skullking_surf.get_width()//2, self.height//2 - skullking_surf.get_height()//2))
        
        # Add a start button
        return start_surf

#%% BUTTONS

    def get_start_button(self):
        div = self.height//10
        self.start_button = Button(self.screen, self.width//2-div, (5*self.height)//6, 2*div, div, text='Start', fontSize=div//2, margin=div, inactiveColour=(128, 128, 128), hoverColour=(255, 0, 0), pressedColour=(0, 255, 0), onClick=self.on_start_button_click, radius=20)
    
    def get_bet_slider(self, hand:CardCollection):
        x_margin = self.width//30
        y_margin = self.height//30
        x = self.width//6 + x_margin
        y = (7*self.height//10) + y_margin
        w = (4*self.width)//6 - (2*x_margin)
        h = self.height//10 - (2*y_margin)
        self.bet_slider = Slider(self.screen, x, y, w, h, min=0, max=len(hand), step=1, initial=0, handleColour=self.colors["green"])
    
    def get_bet_button(self):
        x_margin = self.width//40
        y_margin = self.height//60
        x = (5*self.width)//6 + x_margin
        y = (7*self.height//10) + y_margin
        w = (self.width)//6 - (2*x_margin)
        h = self.height//10 - (2*y_margin)
        self.bet_button = Button(self.screen, x, y, w, h, text='Bet', onClick=self.on_bet_click, radius=20, hoverColour=self.colors["green"], inactiveColour=self.colors["white"])


#%% EVENTS

    def on_bet_click(self):
        self.bet = self.bet_slider.getValue()
    
    def on_closing(self):
        pygame.quit()
        exit()
        
    def on_start_button_click(self):
        self.clicked_start = True

#%% UTILS

    def draw_text(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))