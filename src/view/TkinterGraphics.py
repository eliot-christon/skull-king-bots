__author__ = 'Eliot Christon'
__email__ = 'eliot.christon@gmail.com'

from .Graphics import Graphics
from ..model.Game import Game

import tkinter as tk
from PIL import Image, ImageTk
import os


class TkinterGraphics(Graphics):
    """TkinterGraphics class for the Skull King game"""

    def __init__(self, game:Game, assets_folder:str) -> None:
        super().__init__(game=game)
        self.assets_folder = assets_folder
        self.card_images = self.load_card_images()
        
        self.root = tk.Tk()
        self.root.title("Skull King Game")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.render()
        self.root.mainloop()

    def load_card_images(self) -> dict:
        """Load all card images from the assets folder"""
        card_images = {}
        for filename in os.listdir(self.assets_folder):
            if filename.endswith(".png"):
                card_name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.assets_folder, filename)
                image = Image.open(image_path)
                card_images[card_name] = ImageTk.PhotoImage(image)
        return card_images

    def render(self) -> None:
        """Render the game using Tkinter"""
        self.canvas.delete("all")
        self.render_game_info()
        self.render_players()
        self.root.update()

    def render_game_info(self) -> None:
        """Render the game info like round and state"""
        game_info = f"Round: {self._game.round}, State: {self._game.current_state}"
        self.canvas.create_text(400, 20, text=game_info, font=("Arial", 20))

    def render_players(self) -> None:
        """Render the players and their information"""
        spacing = [15, 5, 6]
        y_offset = 50
        self.canvas.create_text(400, y_offset, text="Player name | Score | Tricks | Hand", font=("Arial", 16))
        y_offset += 30

        for player in self._game.players:
            player_info = f"{player.name} | {player.score} | {player.tricks} / {player.bet}"
            self.canvas.create_text(150, y_offset, text=player_info, anchor="w", font=("Arial", 14))
            
            x_offset = 300
            for card in player.hand:
                card_image = self.card_images.get(card, None)
                if card_image:
                    self.canvas.create_image(x_offset, y_offset, image=card_image, anchor="w")
                x_offset += 60

            y_offset += 50
