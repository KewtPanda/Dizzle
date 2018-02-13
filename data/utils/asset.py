"""
Asset Module

This module defines functions for loading resource files for use
with the game and the level editor.
"""

import os
import sys
import json
import shelve
import pygame
from pygame.locals import *
from data.utils.constants import IMAGE_PATH, SOUND_PATH, MUSIC_PATH, LEVEL_PATH, HIGHSCORE_FILE, KB_KEYS, JS_KEYS,\
    CONTROLS, STD_CONTROLS, BG_COLOR, RESOLUTION
from data.utils.colors import *
from data.game.button import *
from data.game.square import *

global name
name = ''


def load_image(file_name):
    """Load an image and return the image object and the image rect."""
    path = os.path.join(IMAGE_PATH, file_name)
    path = os.path.abspath(path)

    try:
        image = pygame.image.load(path)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as e:
        print('Could not load image: ', path)
        print(e)
        raise SystemExit

    return image, image.get_rect()


def load_sound(file_name):
    """Load a sound and return the sound object."""
    path = os.path.join(SOUND_PATH, file_name)
    path = os.path.abspath(path)

    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error as e:
        print('Could not load sound: ', path)
        print(e)
        raise SystemExit

    return sound


def load_music(file_name):
    """Load a sound and return the sound object."""
    path = os.path.join(MUSIC_PATH, file_name)
    path = os.path.abspath(path)

    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error as e:
        print('Could not load sound: ', path)
        print(e)
        raise SystemExit

    return sound


def load_level(file_name):
    """Load the given json level file into a dict and return the dict."""
    path = os.path.join(LEVEL_PATH, file_name)
    path = os.path.abspath(path)

    with open(path, 'r') as f:
        level = json.load(f)

    return level


def save_level(level, file_name):
    """Write the given level to the given json file."""
    with open(file_name, 'w') as f:
        json.dump(level, f, indent=4)


def load_highscore(score, SCREEN, FONT_30, FONT_60):
    """Load the highscore, check if new score is big enough to be on it, and return highscore."""
    hs = shelve.open(HIGHSCORE_FILE)  # open file
    key = 'highscore'  # what to check for in file
    top_list = 10  # number of ranks in highscore file

    # if no highscore exist, create a new one
    if key not in hs:
        new_highscore = [[0 for x in range(2)] for y in
                         range(top_list)]  # create a new matrix with the size 10 x 2 (TOP 10, with name and score)
        for row in range(top_list):
            new_highscore[row][0] = 'blank'  # set the name in new highscore to blank
        hs[key] = new_highscore

    highscore = hs['highscore']  # get current highscores

    # check if new score is high enough to get on highscore
    for row in range(top_list):
        if score > highscore[row][1]:
            set_name(SCREEN, FONT_30, FONT_60)
            name_score = (name, score)
            highscore.insert(row, name_score)  # insert name and score inside the highscore
            highscore.pop()  # removes the last item on the highscore
            break

    hs[key] = highscore  # save new highscore
    hs.close()  # close file
    return highscore


def get_events(mode=1):
    joystick_button = False
    keys = []
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # check user event - SONG ENDED
        elif event.type == pygame.USEREVENT + 1:
            CONTROLS['next_song'] = True
        # check if mouse is clicked
        elif event.type == MOUSEBUTTONUP:
            CONTROLS['accept'] = True
        # check if keyboard is clicked and what key
        elif event.type == KEYDOWN:
            if event.key in KB_KEYS:
                CONTROLS[KB_KEYS[event.key]] = True
            if event.unicode.isalpha():
                keys.append(event.unicode)
        # check if joystick button is clicked
        elif event.type == JOYBUTTONDOWN:
            # check joystick buttons
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()

                # Buttons
                buttons = joystick.get_numbuttons()
                for j in range(buttons):
                    if joystick.get_button(j) and j in JS_KEYS:
                        CONTROLS[JS_KEYS[j]] = True

    # check if c or q is pressed to close the game
    if CONTROLS['close']:
        pygame.quit()
        sys.exit()

    if mode == 1:
        CONTROLS['mouse'] = pygame.mouse.get_pos()
        try:
            # check joystick controls
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()

                # Axes
                axes = joystick.get_numaxes()
            
                for j in range(axes):
                    axis = joystick.get_axis(j)
                    if j == 0 and axis < 0:
                        CONTROLS['left'] = True
                    elif j == 0 and axis > 0:
                        CONTROLS['right'] = True
                    if j == 1 and axis > 0:
                        CONTROLS['down'] = True
                    elif j == 1 and axis < 0:
                        CONTROLS['up'] = True

                # Hat switch. All or nothing for direction.
                hats = joystick.get_numhats()
                for j in range(hats):
                    hat = joystick.get_hat(j)
                    if hat[0] < 0:
                        CONTROLS['left'] = True
                    elif hat[0] > 0:
                        CONTROLS['right'] = True
                    if hat[1] < 0:
                        CONTROLS['down'] = True
                    elif hat[1] > 0:
                        CONTROLS['up'] = True
        except:
            print('Something went wrong with joystick event')

    return keys


def del_events():
    for key in CONTROLS:
        CONTROLS[key] = STD_CONTROLS[key]


def set_name(SCREEN, FONT_30, FONT_60):
    FPS_CLOCK = pygame.time.Clock()
    global name
    text = 'Enter Name Below'
    letter = 'A'
    cap_letters = True
    time_last = 0
    while True:
        del_events()
        keys = get_events()

        time_now = pygame.time.get_ticks()
        if CONTROLS['right'] and (time_now > time_last + 100):
            name += letter
            time_last = time_now
        elif CONTROLS['up'] and (time_now > time_last + 100):
            letter = chr(ord(letter) + 1)
            time_last = time_now
        elif CONTROLS['down'] and (time_now > time_last + 100):
            letter = chr(ord(letter) - 1)
            time_last = time_now
        elif CONTROLS['erase']:
            name = name[:-1]
        elif CONTROLS['back']:
            letter = 'A'
        elif CONTROLS['accept']:
            popup = pygame.sprite.Group()
            popup.add(Square(width=800, height=400, position=(RESOLUTION[0]/2-800/2, RESOLUTION[1]/2-400/2), color=COLORS[GRAY]))
            popup.draw(SCREEN)

            text_name = FONT_30.render("Is your name " + str(name) + "?", True, COLORS[WHITE])
            SCREEN.blit(text_name, (RESOLUTION[0] / 2 - 400 / 2, 200))

            x = 300
            y = 500
            pos = [x, y]
            last_mouse = pygame.mouse.get_pos()

            buttons_group = pygame.sprite.Group()
            buttons = []
            b = Button(width=50, position=(x-1, y-1), box_color=COLORS[GRAY], text="Yes")
            buttons_group.add(b)
            buttons.append(b)
            b = Button(width=50, position=(x - 1 + 650, y - 1), box_color=COLORS[GRAY], text="No")
            buttons_group.add(b)
            buttons.append(b)

            while True:
                del_events()
                get_events()

                if CONTROLS['mouse'] != last_mouse:
                    pos[0] = 0
                    last_mouse = CONTROLS['mouse']

                if CONTROLS['right']:
                    if x < 500:
                        x += 650
                        pos[0] = x
                    time_last = time_now
                elif CONTROLS['left']:
                    if x > 500:
                        x -= 650
                        pos[0] = x
                elif CONTROLS['back']:
                    break
                elif CONTROLS['accept']:
                    if buttons[0].rect.collidepoint(CONTROLS['mouse']) or buttons[0].rect.collidepoint(pos):
                        return
                    elif buttons[1].rect.collidepoint(CONTROLS['mouse']) or buttons[1].rect.collidepoint(pos):
                        break
                buttons_group.update(pos)
                buttons_group.draw(SCREEN)
                for button in buttons:
                    button.show_text(SCREEN)

                pygame.display.update()

        elif CONTROLS['misc']:
            if cap_letters:
                cap_letters = False
                letter = chr(ord(letter) + 32)
            elif not cap_letters:
                cap_letters = True
                letter = chr(ord(letter) - 32)

        # write letters from keyboard
        for key in keys:
            name += key

        SCREEN.fill(COLORS[BG_COLOR])
        # put text on screen
        block = FONT_30.render(text, True, COLORS[WHITE])
        rect = block.get_rect()
        rect.center = SCREEN.get_rect().center
        SCREEN.blit(block, (rect[0], rect[1] - 150))
        # put name on screen
        block = FONT_30.render(name, True, COLORS[WHITE])
        rect = block.get_rect()
        rect.center = SCREEN.get_rect().center
        SCREEN.blit(block, rect)
        # put letter on screen
        block = FONT_30.render(letter, True, COLORS[WHITE])
        rect.center = SCREEN.get_rect().center
        SCREEN.blit(block, (rect[0], rect[1] - 50))
        # update display
        pygame.display.update()
        FPS_CLOCK.tick(60)
