"""
Editor Module

This module defines the Editor class. This module runs
the game's level editor.
"""

import sys, os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import data.utils.asset as asset
from data.utils.constants import START_LEVEL, LEVEL_PATH
from data.editor.brick import BrickFrame
from data.editor.entry import EntryFrame


class Editor(tk.Frame):
    """Main level editor frame."""

    def __init__(self, parent):
        """Initialize the editor."""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.level_filename = START_LEVEL
        self.parent.title('Breakout Editor - ' + self.level_filename)
        self.level = asset.load_level(self.level_filename)

        self.grid()
        self.create_widgets()
        self.grid_widgets()

    def create_widgets(self):
        """Create editor frame widgets."""
        # create file menu
        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label='New', command=self.new_level)
        self.file_menu.add_command(label='Open', command=self.open_level)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=self.save_level)
        self.file_menu.add_command(label='Save as', command=self.save_level_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit)
        self.menu.add_cascade(label='File', menu=self.file_menu)

        # create input boxes
        self.entry_frame = EntryFrame(self, self.level)

        # create brick button grid
        self.brick_frame = BrickFrame(self, self.level['bricks'], self.entry_frame.color_option)

    def grid_widgets(self):
        """position widgets in the frame."""
        self.brick_frame.grid(row=0, column=0)
        self.brick_frame['pady'] = 35
        self.brick_frame['padx'] = 10
        self.entry_frame.grid(row=1, column=0)

    def save_level(self):
        """Save the level under the current level name."""
        if self.level_filename == 'untitled.json':
            self.save_level_as();
        else:
            level = {
                'bricks': self.brick_frame.bricks
            }
            asset.save_level(level, os.path.join(LEVEL_PATH, self.level_filename))

    def save_level_as(self):
        """Save the level file."""
        filename = asksaveasfilename(initialdir=LEVEL_PATH, initialfile=self.level_filename)
        if filename != '':
            self.level_filename = filename
            level = {
                'bricks': self.brick_frame.bricks
            }
            asset.save_level(level, self.level_filename)
            self.parent.title('Breakout Editor - ' + os.path.basename(self.level_filename))

    def open_level(self):
        """Open the level file."""
        filename = askopenfilename(initialdir=LEVEL_PATH, initialfile=self.level_filename)
        if filename != '':
            self.level_filename = filename
            self.parent.title('Breakout Editor - ' + os.path.basename(self.level_filename))
            self.level = asset.load_level(os.path.basename(self.level_filename))
            self.brick_frame.update(self.level['bricks'])
            self.entry_frame.update(self.level)

    def new_level(self):
        """Create a blank level."""
        self.level_filename = START_LEVEL
        self.parent.title('Breakout Editor - ' + self.level_filename)
        self.level = asset.load_level(self.level_filename)
        self.brick_frame.update(self.level['bricks'])
        self.entry_frame.update(self.level)

    def quit(self):
        """Exit the editor."""
        sys.exit()


def run():
    """Run the Editor."""
    root = tk.Tk()
    root.geometry('1500x720')
    editor = Editor(root)
    editor.mainloop()
