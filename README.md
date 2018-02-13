# Dizzle
A breakout game made for Raspberry Pi using Python with Pygame

This is a breakout clone that I made in order to teach
myself about python, pygame, and game development.

Keyboard controls for the game:
Menu:
	- Arrows: move selected menu item
	- Return: goto selected menu item
	- ESC: return to main menu or exit game
Game: 
	- Pause/break: pauses the game
		- Return while paused: options menu
	- ESC: Click 3-4 times to quit to highscore menu
	- Q or C: Close the game
Ball:
	- N: normal ball
	- E: explosion ball
	- L: laser ball
	- P: plasma ball (currently the same as exposion ball)
	- S: snap to paddle
Level:
	- Z: previous level
	- X: next level
Music:
	- V: previous song
	- B: next song
	- M: mute (pause) song
	

### Installation

Python3 and pygame is needed to play this game.

Linux installation:
	sudo apt-get install python3 python3-pygame
	run game by typing (might need sudo):
		python3 dizzle.py
		
	ps. to be able to run the game, you need to be in the Dizzle folder

Windows installation:
	Install python3 from website http://python.org
	Add python3 to environment variables eighter by selecting the option during installation or:
		Right click computer -> Properties -> Advances system settings -> Environment Variables
		Under System variables find Path, click Edit
		Add python3 to the end, something like this:
		;C:\Python34
		Click Ok -> Ok -> Ok
	open cmd (windows+r, then type cmd)
	write:
		python3 -m pip install -U pip			# this updates pip, the package manager for python
		python3 -m pip install pygame --user	# this install pygame
	run game from cmd:
		python3 dizzle.py
	click dizzle.py to start game without cmd
	
	ps. the command in cmd for running python commands might be python instead of python3
	
Level Editor
------------
New levels can be added using the built-in level editor.
Levels must be saved to 'data/assets/levels/' directory
in order to be recognized by the game.

Only the filename is important, ex.
level_1.json
level_2.json
level_3.json

How to make a new level:
Start up the level-editor.
Make changes to the clean level.
Click File -> Save as
Type desired filename (See how to name the file above)
Click Save

ps. The editor can be a bit buggy.
Opening a level and editing it might not work always.
Also clicking new level might not work as intended.
To be safe, open the editor,
edit the clean level that opened,
save the new level with save as,
if you want to create a new level,
restart the editor and do the same as before.

