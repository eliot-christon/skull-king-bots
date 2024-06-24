__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.Card import Card
from src.model.cards.CardCollection import CardCollection
from .Graphics import Graphics
from ..model.Game import Game

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Import messagebox for confirmation dialog
from PIL import Image, ImageTk


class TkinterGraphics(Graphics):
    def __init__(self, root=tk.Tk()):
        super().__init__()
        self.root = root
        self.root.title("Skull King")
        
        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = int(self.root.winfo_screenheight() * 0.9)
        
        # Set window size and position
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#333333')
        self.style.configure('TFrame.TFrame', background='#006666')
        self.style.configure('TLabel', background='#333333', foreground='#ffffff', font=('Arial', 12))
        self.style.configure('TLabel.TLabel', background='#006666', foreground='#ffffff', font=('Arial', 12))
        self.style.configure('TButton', foreground='#ffffff', background='#666666', font=('Arial', 12))

        # Frames
        self.top_frame = ttk.Frame(self.root, style='TFrame')
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.trick_frame = ttk.Frame(self.root)
        self.trick_frame.pack(pady=20)
        
        self.bottom_frame = ttk.Frame(self.root, style='TFrame')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.hand_frame = ttk.Frame(self.bottom_frame, style='TFrame')
        self.hand_frame.pack(side=tk.RIGHT, padx=20)
        
        self.bet_frame = ttk.Frame(self.bottom_frame, style='TFrame')
        self.bet_frame.pack(side=tk.LEFT, padx=20)
        
        self.right_frame = ttk.Frame(self.root, style='TFrame')
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        # Round label
        self.round_label = ttk.Label(self.right_frame, text="Round:1", style='TLabel')
        self.round_label.pack(side=tk.TOP, pady=10)

        # Player frames
        self.player_frames = []

        # Card size
        self.card_size = (100, 150)

        # Variables
        self.selected_card_var = tk.StringVar()
        self.selected_bet_var = tk.IntVar()

        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def render(self, game:Game) -> None:
        # Update round number
        self.round_label.config(text=f"Round:{game.round}")
        
        self.clear_hand()

        # Update middle cards
        self.clear_trick_cards()
        for card in game.trick:
            card_label = self.create_card_label(card)
            card_label.pack(side=tk.LEFT, padx=5)

        # Render players
        self.clear_player_frames()
        for player in game.roll_players( 1 - game.round):
            player_frame = self.create_player_frame(player, game.current_player)
            player_frame.pack(side=tk.LEFT, padx=10)
            self.player_frames.append(player_frame)

        self.root.update()

    def create_card_label(self, card:Card) -> ttk.Label:
        card_path = f"assets/cards/{card.name}.png"
        card_image = Image.open(card_path).resize(self.card_size, Image.Resampling.LANCZOS)
        card_photo = ImageTk.PhotoImage(card_image)
        card_label = ttk.Label(self.trick_frame, image=card_photo)
        card_label.image = card_photo
        return card_label

    def create_player_frame(self, player, current_player) -> ttk.Frame:
        
        player_frame = ttk.Frame(self.top_frame, style='TFrame')
        
        player_name = ttk.Label(player_frame, text=player.name, style='TLabel')
        player_name.pack()

        player_score = ttk.Label(player_frame, text=f"Score:{player.score}", style='TLabel')
        player_score.pack()

        player_tricks = ttk.Label(player_frame, text=f"Tricks:{player.tricks} / {player.bet}", style='TLabel')
        player_tricks.pack()

        player_bonus = ttk.Label(player_frame, text=f"Bonus:{player.bonus}", style='TLabel')
        player_bonus.pack()

        if player == current_player:
            player_frame.configure(style='TFrame.TFrame')  # Highlight current player
            player_name.configure(style='TLabel.TLabel')
            player_score.configure(style='TLabel.TLabel')
            player_tricks.configure(style='TLabel.TLabel')
            player_bonus.configure(style='TLabel.TLabel')

        return player_frame

    def clear_trick_cards(self) -> None:
        for widget in self.trick_frame.winfo_children():
            widget.destroy()

    def clear_player_frames(self) -> None:
        for frame in self.player_frames:
            frame.destroy()
        self.player_frames.clear()

    def choose_card_interaction(self, hand:CardCollection, playable_cards:CardCollection) -> Card:
        self.selected_card_var.set("")  # Reset the selected card variable
        self.render_hand(playable_cards, hand - playable_cards)
        
        # Wait until a card is selected
        self.root.wait_variable(self.selected_card_var)
        
        # Find the selected card object from the card name
        for card in playable_cards:
            if card.name == self.selected_card_var.get():
                return card

    def place_bet(self, hand:CardCollection) -> int:
        self.selected_bet_var.set(-1)  # Reset the selected bet variable
        self.render_bets(hand)
        self.render_hand(hand)
        
        # Wait until a bet is selected
        self.root.wait_variable(self.selected_bet_var)
        
        return self.selected_bet_var.get()
    
    def clear_hand(self) -> None:
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

    def render_hand(self, playable_cards:CardCollection, non_playable_cards:CardCollection=None) -> None:
        self.clear_hand()
            
        for card in playable_cards:
            card_path = f"assets/cards/{card.name}.png"
            card_image = Image.open(card_path).resize(self.card_size, Image.Resampling.LANCZOS)
            card_photo = ImageTk.PhotoImage(card_image)
            card_label = tk.Label(self.hand_frame, image=card_photo)
            card_label.image = card_photo
            card_label.card_name = card.name  # Store card name in the label
            card_label.pack(side=tk.LEFT, padx=5)
            card_label.bind("<Button-1>", self.on_card_click)
        
        if non_playable_cards is not None:
            for card in non_playable_cards:
                card_path = f"assets/cards/{card.name}.png"
                card_image = Image.open(card_path).resize(self.card_size, Image.Resampling.LANCZOS)
                # make it darker
                card_image = card_image.point(lambda p: p * 0.5)
                card_photo = ImageTk.PhotoImage(card_image)
                card_label = tk.Label(self.hand_frame, image=card_photo)
                card_label.image = card_photo
                card_label.pack(side=tk.LEFT, padx=5)

    def render_bets(self, hand:CardCollection) -> None:
        for widget in self.bet_frame.winfo_children():
            widget.destroy()  # Clear previous widgets

        for i in range(len(hand) + 1): # Include 0 as an option
            bet_label = tk.Label(self.bet_frame, text=str(i), padx=10, pady=5, relief=tk.RAISED)
            bet_label.pack(side=tk.LEFT)
            bet_label.bind("<Button-1>", self.on_bet_click)

    def on_card_click(self, event):
        self.selected_card_var.set(event.widget.card_name)  # Set the selected card name
        self.root.quit()  # Exit the main loop

    def on_bet_click(self, event):
        self.selected_bet_var.set(int(event.widget.cget("text")))  # Set the selected bet
        self.root.quit()  # Exit the main loop
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()  # Exit the main loop
            self.root.destroy()
            self._running = False
