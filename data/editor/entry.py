"""
Entry Module
"""

import tkinter as tk

from data.utils.constants import BRICK_IMAGES


class EntryFrame(tk.Frame):
    """Frame containing level attribute entry boxes"""

    def __init__(self, parent, level):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.level = level
        self.colors = sorted(BRICK_IMAGES.keys())

        self.color_option = tk.StringVar()
        self.color_option.set(self.colors[0])

        self.create_widgets()
        self.grid_widgets()

    def create_widgets(self):
        """Create frame widgets"""
        self.color_label = tk.Label(self, text='Brick Color:')
        self.color_dropdown = tk.OptionMenu(self, self.color_option, *self.colors)

    def grid_widgets(self):
        """Postition frame widgets"""
        self.color_label.grid(row=0, column=0, stick='W', padx=50)
        self.color_dropdown.grid(row=1, column=0, sticky='W', padx=50)


    def update(self, level):
        """Update the frame with new level info."""
        self.level = level

