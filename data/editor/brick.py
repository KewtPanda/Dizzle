"""
Brick Module
"""

import os
import tkinter as tk

from data.utils.constants import BRICK_IMAGES, IMAGE_PATH


class BrickFrame(tk.Frame):
    """Frame that contains grid of brick buttons"""
    def __init__(self, parent, bricks, color_option):
        """Initialze the button grid"""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.bricks = bricks
        self.color_option = color_option
        self.buttons = []
        self.images = {}
        self.init_images()
        self.create_widgets()
        self.grid_widgets()


    def create_widgets(self):
        """create grid of buttons"""
        for i, row in enumerate(self.bricks):
            btn_row = []
            for j, color in enumerate(row):
                brick_img = self.images[color]
                button = tk.Button(self, image=brick_img, width=30, height=12)
                button.image = brick_img
                button.config(command=lambda x=i, y=j: self.change_color(x, y))
                btn_row.append(button)

            self.buttons.append(btn_row)


    def grid_widgets(self):
        """Position buttons."""
        for y, button_row in enumerate(self.buttons):
            for x, button in enumerate(button_row):
                button.grid(row=y, column=x)


    def change_color(self, i, j):
        """Change the color of the brick when clicked."""
        color = self.color_option.get()
        brick_img = self.images[color]
        self.buttons[i][j].configure(image=brick_img)
        self.buttons[i][j].image = brick_img
        self.bricks[i][j] = color


    def init_images(self):
        """save tk.PhotoImages into dictionary."""
        for color in BRICK_IMAGES.keys():
            img_path = os.path.join(IMAGE_PATH, BRICK_IMAGES[color])
            self.images.update({color: tk.PhotoImage(file=img_path)})


    def update(self, bricks):
        """Update frame with new level info."""
        for row1, row2 in zip(self.buttons, bricks):
            for button, color in zip(row1, row2):
                button.config(image=self.images[color])
