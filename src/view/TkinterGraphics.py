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
from typing import List, Dict
import os


class TkinterGraphics(Graphics):
    def __init__(self, root=tk.Tk()):
        super().__init__()

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#333333')
        self.style.configure('CurrentPlayer.TFrame', background='#006666')
        self.style.configure('Grid.TFrame', background='#333333', foreground='#ffffff', font=('Arial', 16))
        self.style.configure('TLabel', background='#333333', foreground='#ffffff', font=('Arial', 12))
        self.style.configure('CurrentPlayer.TLabel', background='#006666', foreground='#ffffff', font=('Arial', 12))
        self.style.configure('TButton', foreground='#ffffff', background='#666666', font=('Arial', 12))
        self.style.configure('Quit.TButton', background='#ffffff', foreground='#ee1122', font=('Arial', 16))

        self.root = root
        self.root.title("Skull King")
        self.root.configure(bg='#333333')
        
        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = int(self.root.winfo_screenheight() * 0.9)
        
        # Set window size and position
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

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
        for player in game.players:
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
            player_frame.configure(style='CurrentPlayer.TFrame')  # Highlight current player
            player_name.configure(style='CurrentPlayer.TLabel')
            player_score.configure(style='CurrentPlayer.TLabel')
            player_tricks.configure(style='CurrentPlayer.TLabel')
            player_bonus.configure(style='CurrentPlayer.TLabel')

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

    def display_history(self, history:List[Dict[str, Dict[str, int]]]) -> None:
        # clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, style='TFrame')
        frame.pack(pady=20)

        player_names = list(history[0].keys())
        
        # Create header
        round_label = ttk.Label(frame, text="Round", font=('Helvetica', 10, 'bold'))
        round_label.grid(row=1, column=0, padx=5, pady=5)

        col = 2
        for player_name in player_names:
            player_label = ttk.Label(frame, text=player_name, font=('Helvetica', 14, 'bold'))
            player_label.grid(row=0, column=col, columnspan=3, padx=5, pady=5)
            
            score_label = ttk.Label(frame, text="Score", font=('Helvetica', 7, 'italic'))
            score_label.grid(row=1, column=col, padx=5, pady=5)
            
            tricks_bet_label = ttk.Label(frame, text="Tricks/Bet", font=('Helvetica', 7, 'italic'))
            tricks_bet_label.grid(row=1, column=col + 1, padx=5, pady=5)
            
            bonus_label = ttk.Label(frame, text="Bonus", font=('Helvetica', 7, 'italic'))
            bonus_label.grid(row=1, column=col + 2, padx=5, pady=5)
            
            col += 4

        # Add a horizontal separator after the header
        ttk.Separator(frame, orient='horizontal').grid(row=2, column=0, columnspan=col, sticky='ew', pady=5)

        # Create rows for each round
        for round_num, round_history in enumerate(history):
            round_num_label = ttk.Label(frame, text=f"{round_num + 1}", font=('Helvetica', 14))
            round_num_label.grid(row=(round_num * 2) + 3, column=0, padx=5, pady=5)

            col = 2
            for player_name in player_names:
                player_history = round_history[player_name]
                score = player_history['score']
                tricks = player_history['tricks']
                bet = player_history['bet']
                bonus = player_history['bonus']

                score_label = ttk.Label(frame, text=f"{score}", font=('Helvetica', 10, 'bold'))
                score_label.grid(row=(round_num * 2) + 3, column=col, padx=5, pady=5)
                
                tricks_bet_label = ttk.Label(frame, text=f"{tricks}/{bet}", font=('Helvetica', 9))
                tricks_bet_label.grid(row=(round_num * 2) + 3, column=col + 1, padx=5, pady=5)
                
                bonus_label = ttk.Label(frame, text=f"{bonus}" if bonus > 0 else "", font=('Helvetica', 9))
                bonus_label.grid(row=(round_num * 2) + 3, column=col + 2, padx=5, pady=5)
                
                col += 4

            # Add a horizontal separator after each round
            ttk.Separator(frame, orient='horizontal').grid(row=(round_num * 2) + 4, column=0, columnspan=col, sticky='ew', pady=5)

        # Add vertical separators between columns
        for col_num in range(1, col, 4):
            ttk.Separator(frame, orient='vertical').grid(row=0, column=col_num, rowspan=(len(history) * 2) + 2, sticky='ns')


        # display the quit button
        quit_button = ttk.Button(self.root, text="Quit", command=self.on_closing)
        quit_button.configure(style='Quit.TButton')
        quit_button.pack()
        self.root.mainloop()
