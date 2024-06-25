__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from typing import List, Dict
from src.model.cards.Card import Card
from src.model.cards.CardCollection import CardCollection
from .Graphics import Graphics
from ..model.Game import Game


class TkinterGraphics(Graphics):
    def __init__(self, root=tk.Tk()):
        super().__init__()
        self.root = root
        self.root.title("Skull King")

        self.style = self.configure_styles()
        self.card_size = (100, 150)
        self.selected_card_var = tk.StringVar()
        self.selected_bet_var = tk.IntVar()
        self.click_on_start = tk.BooleanVar()

        self.player_frames = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#333333')
        style.configure('CurrentPlayer.TFrame', background='#006666')
        style.configure('Grid.TFrame', background='#333333', foreground='#ffffff', font=('Arial', 16))
        style.configure('TLabel', background='#333333', foreground='#ffffff', font=('Arial', 12))
        style.configure('CurrentPlayer.TLabel', background='#006666', foreground='#ffffff', font=('Arial', 12))
        style.configure('TButton', foreground='#ffffff', background='#666666', font=('Arial', 12))
        style.configure('Start.TButton', background='#ffffff', foreground='#22ee11', font=('Arial', 16))
        style.configure('Quit.TButton', background='#ffffff', foreground='#ee1122', font=('Arial', 16))
        return style

    def setup(self):
        self.root.configure(bg='#333333')
        screen_width = int(self.root.winfo_screenwidth() * 0.8)
        screen_height = int(self.root.winfo_screenheight() * 0.6)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

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

        self.round_label = ttk.Label(self.right_frame, text="Round:1", style='TLabel')
        self.round_label.pack(side=tk.TOP, pady=10)

    def render(self, game: Game) -> None:
        self.round_label.config(text=f"Round:{game.round}")
        self.clear_hand()
        self.clear_trick_cards()
        self.display_trick_cards(game.trick)
        self.render_players(game)

    def display_trick_cards(self, trick: CardCollection):
        for card in trick:
            card_label = self.create_card_label(card)
            card_label.pack(side=tk.LEFT, padx=5)

    def render_players(self, game: Game):
        self.clear_player_frames()
        for player in game.players:
            player_frame = self.create_player_frame(player, game.current_player)
            player_frame.pack(side=tk.LEFT, padx=10)
            self.player_frames.append(player_frame)
        self.root.update()

    def create_card_label(self, card: Card) -> ttk.Label:
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
            self.highlight_current_player(player_frame, player_name, player_score, player_tricks, player_bonus)

        return player_frame

    def highlight_current_player(self, *widgets):
        for widget in widgets:
            widget.configure(style='CurrentPlayer.TLabel')

    def clear_trick_cards(self) -> None:
        for widget in self.trick_frame.winfo_children():
            widget.destroy()

    def clear_player_frames(self) -> None:
        for frame in self.player_frames:
            frame.destroy()
        self.player_frames.clear()

    def choose_card_interaction(self, hand: CardCollection, playable_cards: CardCollection) -> Card:
        self.selected_card_var.set("")
        self.render_hand(playable_cards, hand - playable_cards)
        self.root.wait_variable(self.selected_card_var)
        return self.get_selected_card(playable_cards)

    def get_selected_card(self, playable_cards: CardCollection) -> Card:
        for card in playable_cards:
            if card.name == self.selected_card_var.get():
                return card

    def place_bet(self, hand: CardCollection) -> int:
        self.selected_bet_var.set(-1)
        self.render_bets(hand)
        self.render_hand(hand)
        self.root.wait_variable(self.selected_bet_var)
        return self.selected_bet_var.get()

    def clear_hand(self) -> None:
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

    def render_hand(self, playable_cards: CardCollection, non_playable_cards: CardCollection = None) -> None:
        self.clear_hand()
        self.display_hand(playable_cards, self.on_card_click)

        if non_playable_cards:
            self.display_hand(non_playable_cards, self.on_card_click, make_darker=True)

    def display_hand(self, cards: CardCollection, click_callback, make_darker=False):
        for card in cards:
            card_label = self.create_card_label(card, make_darker)
            card_label.pack(side=tk.LEFT, padx=5)
            card_label.bind("<Button-1>", click_callback)

    def create_card_label(self, card: Card, make_darker=False) -> tk.Label:
        card_path = f"assets/cards/{card.name}.png"
        card_image = Image.open(card_path).resize(self.card_size, Image.Resampling.LANCZOS)
        if make_darker:
            card_image = card_image.point(lambda p: p * 0.5)
        card_photo = ImageTk.PhotoImage(card_image)
        card_label = tk.Label(self.hand_frame, image=card_photo)
        card_label.image = card_photo
        card_label.card_name = card.name
        return card_label

    def render_bets(self, hand: CardCollection) -> None:
        self.clear_frame(self.bet_frame)
        for i in range(len(hand) + 1):
            bet_label = tk.Label(self.bet_frame, text=str(i), padx=10, pady=5, relief=tk.RAISED)
            bet_label.pack(side=tk.LEFT)
            bet_label.bind("<Button-1>", self.on_bet_click)

    def clear_frame(self, frame: ttk.Frame) -> None:
        for widget in frame.winfo_children():
            widget.destroy()

    def on_card_click(self, event):
        self.selected_card_var.set(event.widget.card_name)
        self.root.quit()

    def on_bet_click(self, event):
        self.selected_bet_var.set(int(event.widget.cget("text")))
        self.root.quit()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()

    def on_start_button_click(self):
        self.click_on_start.set(True)

    def start_screen(self) -> None:
        self.clear_screen()
        self.display_background("assets/cards/back.png")
        self.create_start_button()
        self.root.wait_variable(self.click_on_start)
        self.clear_screen()
        self.setup()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_background(self, image_path: str):
        background_image = Image.open(image_path)
        self.root.geometry(f"{background_image.width}x{background_image.height}")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)
        background_label.image = background_photo
        background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_start_button(self):
        start_button = ttk.Button(self.root, text="Start", style="Start.TButton", command=self.on_start_button_click)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the start button

    def start(self):
        self.root.mainloop()

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
