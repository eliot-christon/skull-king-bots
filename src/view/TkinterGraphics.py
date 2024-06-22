__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from src.model.cards.Card import Card
from src.model.cards.CardCollection import CardCollection
from .Graphics import Graphics
from ..model.Game import Game

import tkinter as tk
from tkinter import messagebox  # Import messagebox for confirmation dialog
from PIL import Image, ImageTk


class TkinterGraphics(Graphics):
    def __init__(self, root=tk.Tk()):
        super().__init__()
        self.root = root
        self.root.title("Skull King")
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size to occupy the entire screen
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Configure window to be resizable (optional)
        self.root.resizable(True, True)

        # Top frame for score and round number
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, pady=10)

        self.round_label = tk.Label(self.top_frame, text="Round: 1")
        self.round_label.pack(side=tk.RIGHT, padx=20)

        # Trick frame for the trick cards
        self.trick_frame = tk.Frame(self.root)
        self.trick_frame.pack(pady=20)
        
        # Bottom frame
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=20)

        # Hand frame for the hand cards
        self.hand_frame = tk.Frame(self.bottom_frame)
        self.hand_frame.pack(side=tk.RIGHT, pady=20)
        
        # Bet frame for the bet options
        self.bet_frame = tk.Frame(self.bottom_frame)
        self.bet_frame.pack(side=tk.LEFT, pady=20)

        # Right frame for all players
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        self.middle_cards = []
        self.bottom_cards = []

        self.card_size = (100, 150)  # Resize dimensions (width, height)

        self.selected_card_var = tk.StringVar()  # Variable to track the selected card
        self.selected_bet_var = tk.IntVar()  # Variable to track the selected bet
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def render(self, game: Game) -> None:
        """Render the game in the GUI"""
        # Update the round number
        self.round_label.config(text=f"Round: {game.round}")
        
        # Update the middle cards
        for card_label in self.middle_cards:
            card_label.pack_forget()
        
        self.middle_cards = []
        for card in game.trick:
            card_path = f"assets/cards/{card.name}.png"
            card_image = Image.open(card_path).resize(self.card_size, Image.ANTIALIAS)
            card_photo = ImageTk.PhotoImage(card_image)
            card_label = tk.Label(self.trick_frame, image=card_photo)
            card_label.image = card_photo
            card_label.pack(side=tk.LEFT, padx=5)
            self.middle_cards.append(card_label)
            
        # Display the players
        # highlight the current player
        for widget in self.right_frame.winfo_children():
            widget.destroy()  # Clear previous player frames
            
        for player in game.players:
            player_frame = tk.Frame(self.right_frame)
            player_frame.pack(pady=10)
            
            player_name = tk.Label(player_frame, text=player.name)
            player_name.pack()
            
            player_score = tk.Label(player_frame, text=f"Score: {player.score}")
            player_score.pack()
            
            player_tricks = tk.Label(player_frame, text=f"Tricks: {player.tricks} / {player.bet}")
            player_tricks.pack()
            
            if player == game.current_player:
                player_frame.config(bg="yellow")
            
        self.root.update()

    def choose_card(self, hand: CardCollection, playable_cards: CardCollection) -> Card:
        self.selected_card_var.set("")  # Reset the selected card variable
        self.render_hand(playable_cards)
        
        # Wait until a card is selected
        self.root.wait_variable(self.selected_card_var)
        
        # Find the selected card object from the card name
        for card in playable_cards:
            if card.name == self.selected_card_var.get():
                return card

    def place_bet(self, hand: CardCollection) -> int:
        self.selected_bet_var.set(-1)  # Reset the selected bet variable
        self.render_bets(hand)
        self.render_hand(hand)
        
        # Wait until a bet is selected
        self.root.wait_variable(self.selected_bet_var)
        
        return self.selected_bet_var.get()

    def render_hand(self, playable_cards: CardCollection) -> None:
        for widget in self.hand_frame.winfo_children():
            widget.destroy()  # Clear previous card widgets
            
        for card in playable_cards:
            card_path = f"assets/cards/{card.name}.png"
            card_image = Image.open(card_path).resize(self.card_size, Image.ANTIALIAS)
            card_photo = ImageTk.PhotoImage(card_image)
            card_label = tk.Label(self.hand_frame, image=card_photo)
            card_label.image = card_photo
            card_label.card_name = card.name  # Store card name in the label
            card_label.pack(side=tk.LEFT, padx=5)
            card_label.bind("<Button-1>", self.on_card_click)

    def render_bets(self, hand: CardCollection) -> None:
        for widget in self.bet_frame.winfo_children():
            widget.destroy()  # Clear previous widgets

        for i in range(len(hand) + 1):  # Include 0 as an option
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

    def get_number(self, min: int, max: int, text: str):
        """Get a number from the user"""
        choice = -1
        while choice < min or choice > max:
            try:
                choice = int(input(f"{text} (Between {min} and {max}): "))
            except ValueError:
                print("Please enter a valid number.")
                choice = -1
        return choice
