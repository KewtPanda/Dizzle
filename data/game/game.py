"""
Game module

This module defines the how the game works. 
"""

import sys
import os.path
import time
from pygame.locals import *
from data.utils.constants import GAME_NAME, FPS, BG_COLOR, LEVEL_PATH, MODS, GAME_SOUNDS, CONTROLS, \
    MUSIC_VOLUME, EFFECT_VOLUME, MUSIC_PATH, SOUND_PATH
from data.game.ball import *
from data.game.paddle import *
from data.game.block import *
from data.game.button import *
from data.game.mod import *
from data.utils.asset import load_level, load_highscore, load_music, get_events, del_events
from data.game.player import *
from data.game.playersound import *
import configparser


def menu():
    # texts that will show on screen
    text_name = FONT_60.render('DIZZLE', True, COLORS[WHITE])
    text_menu = ["Start", "Highscore", "Options", "About", "Exit"]

    # menu buttons
    menu_buttons = pygame.sprite.Group()
    buttons = []
    for i in range(len(text_menu)):
        b = Button(position=(RESOLUTION[0] / 2 - 100, 200 + 50 * i), text=text_menu[i])
        menu_buttons.add(b)
        buttons.append(b)

    x_pos = RESOLUTION[0] / 2 - 100
    y_pos = 220
    menu_pos = [x_pos, y_pos]
    last_mouse = pygame.mouse.get_pos()
    time_last = 0
    while True:
        SCREEN.fill(COLORS[BG_COLOR])
        time_now = pygame.time.get_ticks()
        del_events()
        get_events()

        menu_buttons.update(menu_pos)
        menu_buttons.draw(SCREEN)
        for button in buttons:
            button.show_text(SCREEN)

        if CONTROLS['mouse'] != last_mouse:
            menu_pos[0] = 0
            last_mouse = CONTROLS['mouse']
        if CONTROLS['mute']:
            if bg_music.state == 3:
                bg_music.pause()
            elif bg_music.state == 4:
                bg_music.unpause()
        elif CONTROLS['next_song']:
            if not final_song:
                bg_music.next()
        elif CONTROLS['prev_song']:
            bg_music.previous()
        elif CONTROLS['down'] and (time_now > time_last + 100):
            menu_pos[0] = x_pos
            menu_pos[1] += 50
            time_last = time_now
        elif CONTROLS['up'] and (time_now > time_last + 100):
            menu_pos[0] = x_pos
            menu_pos[1] -= 50
            time_last = time_now
        if menu_pos[1] > 450:
            menu_pos[1] = y_pos
        elif menu_pos[1] < y_pos-20:
            menu_pos[1] = 420

        if CONTROLS['accept']:
            for i in range(len(buttons)):
                if buttons[i].rect.collidepoint(CONTROLS['mouse']) or buttons[i].rect.collidepoint(menu_pos):
                    return i

        elif CONTROLS['back']:
            pygame.quit()
            sys.exit()

        SCREEN.blit(text_name, (RESOLUTION[0] / 2 - 100, 50))
        if bg_music.state == 4:
            song_text = FONT_15.render("Music is paused", True, COLORS[WHITE])
            SCREEN.blit(song_text, (500, RESOLUTION[1] - 30))
        elif bg_music.state == 3:
            song_text = FONT_15.render(bg_music.playlist_files[bg_music.track][:-4], True, COLORS[WHITE])
            SCREEN.blit(song_text, (500, RESOLUTION[1]-30))

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def menu_highscore(score):
    highscore = load_highscore(score, SCREEN, FONT_30, FONT_60)  # get highscore, also add new score to the list
    SCREEN.fill(COLORS[BG_COLOR])
    # texts that will show on screen
    text_name = FONT_60.render('HIGHSCORE', True, COLORS[WHITE])
    text_menu = FONT_30.render('Menu', True, COLORS[WHITE])
    text_score = FONT_30.render('Score: ' + str(score), True, COLORS[WHITE])

    # block for menu
    box = pygame.sprite.Group()
    boxes = []
    b = Block(width=100, height=40, position=(0, 0), color=COLORS[BG_COLOR])
    box.add(b)
    boxes.append(b)

    # draw boxes and texts on screen
    box.draw(SCREEN)
    SCREEN.blit(text_name, (RESOLUTION[0] / 2 - 150, 50))
    SCREEN.blit(text_menu, (10, 0))
    SCREEN.blit(text_score, (10, 50))

    for row in range(len(highscore)):
        text_highscore_name = FONT_30.render(highscore[row][0], True, COLORS[WHITE])
        text_highscore = FONT_30.render(str(highscore[row][1]), True, COLORS[WHITE])
        SCREEN.blit(text_highscore_name, (RESOLUTION[0] / 2 - 200, 200 + row * 50))
        SCREEN.blit(text_highscore, (RESOLUTION[0] / 2 + 200, 200 + row * 50))

    while True:
        del_events()
        get_events()
        if CONTROLS['mute']:
            if bg_music.state == 3:
                bg_music.pause()
            elif bg_music.state == 4:
                bg_music.unpause()
        elif CONTROLS['next_song']:
            if not final_song:
                bg_music.next()
        elif CONTROLS['prev_song']:
            bg_music.previous()
        if (CONTROLS['accept'] and boxes[0].rect.collidepoint(CONTROLS['mouse'])) or CONTROLS['back']:
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def menu_options():
    global MUSIC_VOLUME
    global EFFECT_VOLUME
    mus_vol = int(MUSIC_VOLUME * 100)
    eff_vol = int(EFFECT_VOLUME * 100)

    # texts that will show on screen
    text_name = FONT_60.render('OPTIONS', True, COLORS[WHITE])
    text_menu = FONT_30.render('Menu', True, COLORS[WHITE])

    # block for menu
    box = pygame.sprite.Group()
    boxes = []
    b = Block(width=100, height=40, position=(0, 0), color=COLORS[BG_COLOR])
    box.add(b)
    boxes.append(b)

    # buttons
    buttons_group = pygame.sprite.Group()
    buttons = []
    # music volume buttons
    music_down = Button(position=(450, 300), text="MUSIC DOWN")
    music_up = Button(position=(700, 300), text="MUSIC UP")
    buttons_group.add(music_up)
    buttons_group.add(music_down)
    buttons.append(music_up)
    buttons.append(music_down)
    # effect volume buttons
    effect_down = Button(position=(450, 400), text="EFFECT DOWN")
    effect_up = Button(position=(700, 400), text="EFFECT UP")
    buttons_group.add(effect_up)
    buttons_group.add(effect_down)
    buttons.append(effect_up)
    buttons.append(effect_down)

    x_pos = 450
    y_pos = 300
    menu_pos = [x_pos, y_pos]
    last_mouse = pygame.mouse.get_pos()
    time_last = 0

    while True:
        SCREEN.fill(COLORS[BG_COLOR])
        time_now = pygame.time.get_ticks()
        del_events()
        get_events()

        if CONTROLS['mute']:
            if bg_music.state == 3:
                bg_music.pause()
            elif bg_music.state == 4:
                bg_music.unpause()
        elif CONTROLS['next_song']:
            if not final_song:
                bg_music.next()
        elif CONTROLS['prev_song']:
            bg_music.previous()
        if (CONTROLS['accept'] and boxes[0].rect.collidepoint(CONTROLS['mouse'])) or CONTROLS['back']:
            break
        if CONTROLS['mouse'] != last_mouse:
            menu_pos[0] = 0
            last_mouse = CONTROLS['mouse']
        if CONTROLS['down'] and (time_now > time_last + 100):
            menu_pos[1] += 100
            time_last = time_now
            if menu_pos[1] > 450:
                menu_pos[1] = y_pos
        elif CONTROLS['up'] and (time_now > time_last + 100):
            menu_pos[1] -= 100
            time_last = time_now
            if menu_pos[1] < y_pos - 20:
                menu_pos[1] = 300
        elif CONTROLS['left'] and (time_now > time_last + 100):
            menu_pos[0] -= 250
            time_last = time_now
            if menu_pos[0] < x_pos - 20:
                menu_pos[0] = 700
        elif CONTROLS['right'] and (time_now > time_last + 100):
            menu_pos[0] += 250
            time_last = time_now
            if menu_pos[0] > 750:
                menu_pos[0] = x_pos

        buttons_group.update(menu_pos)
        buttons_group.draw(SCREEN)
        for button in buttons:
            button.show_text(SCREEN)
        box.draw(SCREEN)

        if music_up.clicked and MUSIC_VOLUME < 100:
            mus_vol += 1
        elif music_down.clicked and MUSIC_VOLUME > 0:
            mus_vol -= 1
        elif effect_up.clicked and EFFECT_VOLUME < 100:
            eff_vol += 1
        elif effect_down.clicked and EFFECT_VOLUME > 0:
            eff_vol -= 1
        MUSIC_VOLUME = float(mus_vol / 100)
        EFFECT_VOLUME = float(eff_vol/100)

        text_music_volume = FONT_30.render(str(mus_vol), True, COLORS[WHITE])
        text_effect_volume = FONT_30.render(str(eff_vol), True, COLORS[WHITE])

        SCREEN.blit(text_name, (RESOLUTION[0] / 2 - 150, 50))
        SCREEN.blit(text_menu, (10, 0))
        SCREEN.blit(text_music_volume, (350, 300))
        SCREEN.blit(text_effect_volume, (350, 400))

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

    # After menu option closes
    bg_music.set_volume(MUSIC_VOLUME)
    bg_effect.set_volume(EFFECT_VOLUME)
    # save volume to config file
    config = configparser.RawConfigParser()
    config.read("data/assets/config.ini")
    config.set('volume', 'music_volume', str(MUSIC_VOLUME))
    config.set('volume', 'effect_volume', str(EFFECT_VOLUME))
    with open('data/assets/config.ini', 'w') as configfile:
        config.write(configfile)


def menu_about():
    SCREEN.fill(COLORS[BG_COLOR])
    # texts that will show on screen
    text_name = FONT_60.render('ABOUT', True, COLORS[WHITE])
    text_menu = FONT_30.render('Menu', True, COLORS[WHITE])

    # block for menu
    box = pygame.sprite.Group()
    boxes = []
    b = Block(width=100, height=40, position=(0, 0), color=COLORS[BG_COLOR])
    box.add(b)
    boxes.append(b)

    # draw boxes and texts on screen
    box.draw(SCREEN)
    SCREEN.blit(text_name, (RESOLUTION[0] / 2 - 150, 50))
    SCREEN.blit(text_menu, (10, 0))

    # button mapping
    button_mapping_image = pygame.image.load('data/assets/images/button_mapping.png')
    SCREEN.blit(button_mapping_image, (450, 180))
    
    # draw mods on the screen to show their functions
    mod_group = pygame.sprite.Group()
    mods = []
    mod_text = ["Add extra life", "Lose extra life", "Balls become big", "Balls become small", "Balls multiply",
                "Balls snap to paddle", "Paddle size increase", "Paddle size decrease", "Balls get explosion effect",
                "Balls get laser effect"]
    for i in range(len(MODS)):
        m = Mod(SCREEN, position=(30, 200+50*i), block=MODS[i], text=mod_text[i])
        mod_group.add(m)
        mods.append(m)
    mod_group.draw(SCREEN)

    while True:
        del_events()
        get_events()
        if CONTROLS['mute']:
            if bg_music.state == 3:
                bg_music.pause()
            elif bg_music.state == 4:
                bg_music.unpause()
        elif CONTROLS['next_song']:
            if not final_song:
                bg_music.next()
        elif CONTROLS['prev_song']:
            bg_music.previous()
        if (CONTROLS['accept'] and boxes[0].rect.collidepoint(CONTROLS['mouse'])) or CONTROLS['back']:
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


# get level from file and make it into blocks
def get_level(file_name):
    level_frame = load_level(file_name)
    level = level_frame['bricks']
    level_group = pygame.sprite.Group()
    for row in range(len(level)):
        for column in range(len(level[0])):
            if level[row][column] != 'none':
                level_group.add(
                    Block(position=(column * BLOCK_WIDTH + column * 2, 5 * BLOCK_HEIGHT + row * BLOCK_HEIGHT + row * 2),
                          color=COLORS[level[row][column]]))
    return level_group


def run():
    # pre_init(frequency=22050, size=-16, channels=2, buffersize=4096)
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()  # init pygame
    pygame.joystick.init()  # Initialize the joysticks


    # background music
    global bg_music
    bg_music = Player()  # create a new music player running on channel 0
    bg_music.set_endevent(pygame.USEREVENT + 1)  # set end event when playback stop
    bg_music.set_playback_options(play_all=True, loop=True, repeat=False, shuffle=False)
    bg_music.load_folder(MUSIC_PATH)  # load music folder
    bg_music.set_track()  # set track - default 0
    bg_music.set_volume(MUSIC_VOLUME)  # set volume to default, 0.5 (50%)
    bg_music.play()  # start music

    # background effect sounds when losing/winning etc. - Not ball
    global bg_effect
    bg_effect = PlayerSound()
    bg_effect.set_volume(EFFECT_VOLUME)

    global FONT_15
    global FONT_30
    global FONT_60
    FONT_15 = pygame.font.SysFont('Arial', 15)  # setup font
    FONT_30 = pygame.font.SysFont('Arial', 30)  # setup font
    FONT_60 = pygame.font.SysFont('Arial', 60)  # setup font
    global FPS_CLOCK
    FPS_CLOCK = pygame.time.Clock()  # used to manage how fast the screen updates

    # setup the screen
    global SCREEN
    SCREEN = pygame.display.set_mode(RESOLUTION, 0, 32)
    pygame.display.set_caption(GAME_NAME)  # name of the app
    global final_song
    final_song = False
    restart = 1
    while restart == 1:
        # menu
        pygame.mouse.set_visible(True)  # Enable cursor
        pygame.mouse.set_pos(640, 0)
        in_menu = -1
        bg_music.unpause()
        while in_menu != 0:
            in_menu = menu()
            if in_menu == 1:
                menu_highscore(0)
            elif in_menu == 2:
                menu_options()
            elif in_menu == 3:
                menu_about()
            elif in_menu == 4:
                pygame.quit()
                sys.exit()

        # setup paddle
        paddle_color = COLORS[TEAL]
        paddle_width = 100
        paddle_height = 8
        paddle_x = int(RESOLUTION[0] / 2)
        paddle_y = int(RESOLUTION[1] - paddle_height / 2 - 2)
        paddle = Paddle(width=paddle_width, height=paddle_height, position=[paddle_x, paddle_y], color=paddle_color)
        paddle_group = pygame.sprite.Group(paddle)

        # setup ball
        walls = Block(width=RESOLUTION[0], height=1, position=[0, RESOLUTION[1] + 50])
        ball_velocity = [0, -300]
        ball_state = STOP
        ball_group = pygame.sprite.Group()
        ball_group.add(Ball(velocity=ball_velocity, state=ball_state, volume=EFFECT_VOLUME))

        # setup level
        level_files = len([f for f in os.listdir(LEVEL_PATH)
                           if os.path.isfile(os.path.join(LEVEL_PATH, f))])
        level_finished = False
        level_name = 'level_' + str(paddle.level) + '.json'
        level_group = get_level(level_name)

        # setup dizzle
        lives_group = pygame.sprite.Group()
        mods_group = pygame.sprite.Group()

        bg_img = pygame.Surface((1280, 720))
        bg_img.fill(COLORS[BG_COLOR])
        SCREEN.fill(COLORS[BG_COLOR])
        pygame.display.update()
        old_rects = []
        old_rects_lvl = []

        pygame.mouse.set_visible(False)  # disable cursor
        stop_time = pygame.time.get_ticks()  # used to check how long between each time back button is pressed ingame
        stop_game_count = 0  # used to count how many times back button is pressed ingame
        game_loop = 1
        # main game loop
        while game_loop == 1:
            # get events
            del_events()
            get_events(mode=0)

            rects = []
            if CONTROLS['mute']:
                if bg_music.state == 3:
                    bg_music.pause()
                elif bg_music.state == 4:
                    bg_music.unpause()
            elif CONTROLS['next_song']:
                if not final_song:
                    bg_music.next()
            elif CONTROLS['prev_song']:
                bg_music.previous()
            elif CONTROLS['back']:
                time_now = pygame.time.get_ticks()
                if stop_game_count > 2:
                    pygame.mouse.set_visible(True)  # Enable cursor
                    menu_highscore(paddle.score)
                    game_loop = 0
                if time_now > stop_time + 5000:
                    stop_game_count = 0
                stop_game_count += 1
                stop_time = pygame.time.get_ticks()

            elif CONTROLS['pause']:
                cur_pos = pygame.mouse.get_pos()
                while True:
                    del_events()
                    get_events()
                    pygame.mouse.set_pos(cur_pos)

                    if CONTROLS['mute']:
                        if bg_music.state == 3:
                            bg_music.pause()
                        elif bg_music.state == 4:
                            bg_music.unpause()
                    elif CONTROLS['next_song']:
                        if not final_song:
                            bg_music.next()
                    elif CONTROLS['prev_song']:
                        bg_music.previous()
                    if CONTROLS['pause']:
                        break
                    elif CONTROLS['accept']:
                        pygame.mouse.set_visible(True)
                        menu_options()
                        pygame.mouse.set_visible(False)

                    SCREEN.fill(COLORS[BG_COLOR])
                    paddle_group.update()

                    text_pause = FONT_60.render('PAUSE', True, COLORS[WHITE])
                    rects += [SCREEN.blit(text_pause, (RESOLUTION[0] / 2 - 80, RESOLUTION[1] / 2))]
                    SCREEN.blit(score_text, (10, 10))
                    SCREEN.blit(level_text, (RESOLUTION[0] - 120, 10))
                    if bg_music.state == 4:
                        song_text = FONT_15.render("Music is paused", True, paddle_color)
                        SCREEN.blit(song_text, (500, 5))
                    elif bg_music.state == 3:
                        song_text = FONT_15.render(bg_music.playlist_files[bg_music.track][:-4], True, paddle_color)
                        SCREEN.blit(song_text, (500, 5))
                    lives_group.draw(SCREEN)
                    paddle_group.draw(SCREEN)
                    ball_group.draw(SCREEN)
                    level_group.draw(SCREEN)
                    mods_group.draw(SCREEN)

                    pygame.display.update()

                    FPS_CLOCK.tick(FPS)
            elif CONTROLS['next_level']:
                paddle.level += 1
                level_finished = True
            elif CONTROLS['prev_level']:
                paddle.level -= 1
                if paddle.level < 1:
                    paddle.level = 1
                level_finished = True
            elif CONTROLS['snap_ball']:
                for balls in ball_group:
                    balls.state = SNAP
            elif CONTROLS['normal_ball']:
                for balls in ball_group:
                    balls.color = WHITE
                    balls.change_effect(volume=EFFECT_VOLUME)
            elif CONTROLS['explosion_ball']:
                for balls in ball_group:
                    balls.color = RED
                    balls.change_effect(volume=EFFECT_VOLUME)
            elif CONTROLS['laser_ball']:
                for balls in ball_group:
                    balls.color = BLUE
                    balls.change_effect(volume=EFFECT_VOLUME)
            elif CONTROLS['plasma_ball']:
                for balls in ball_group:
                    balls.color = RED
                    balls.change_effect(volume=EFFECT_VOLUME)

            final_song = False
            # clear the screen
            SCREEN.fill(COLORS[BG_COLOR])

            # check if map is finished
            if not level_group.has(level_group) or paddle.lives < 0:
                paddle.level += 1
                level_finished = True

            if level_finished:
                level_finished = False
                level_group.empty()
                ball_group.empty()
                old_rects_lvl = []
                old_rects = []
                SCREEN.fill(COLORS[BG_COLOR])
                pygame.display.update()
                if paddle.level >= level_files or paddle.lives < 0:
                    # get right music
                    if paddle.level >= level_files and paddle.lives >= 0:
                        bg_music.pause()
                        bg_effect.load_sound(SOUND_PATH + GAME_SOUNDS['victory'])
                    elif paddle.lives < 0:
                        bg_music.pause()
                        bg_effect.load_sound(SOUND_PATH + GAME_SOUNDS['lose'])
                    if paddle.lives > 0:
                        paddle.score = paddle.score + paddle.lives * 10  # increase score for each life left
                    pygame.mouse.set_visible(True)  # Enable cursor
                    menu_highscore(paddle.score)
                    game_loop = 0
                else:
                    ball_group.add(Ball(velocity=ball_velocity, state=ball_state, volume=EFFECT_VOLUME))
                    level_name = 'level_' + str(paddle.level) + '.json'
                    level_group = get_level(level_name)
                    if paddle.level >= level_files-1:
                        bg_music.load_sound(SOUND_PATH + GAME_SOUNDS['final'])
                        final_song = True
            # check if ball goes out of bounds (bottom)
            if pygame.sprite.spritecollide(walls, ball_group, True):
                if not ball_group.has(ball_group):
                    paddle.lives -= 1
                    if paddle.lives >= 0:
                        ball_group.add(Ball(velocity=ball_velocity, state=ball_state, volume=EFFECT_VOLUME))
                    else:
                        level_finished = True

            # update sprites/objects
            paddle_group.update()
            for ball in ball_group:
                pos = ball.update(paddle, level_group, ball, CONTROLS['accept'])
                if pos is not None:
                    mods_group.add(Block(position=pos, mod=MODS[random.randint(0, len(MODS) - 1)]))
            # pos = ball_group.update(paddle, level_group, ball_group)
            mods_group.update(mods_group, paddle, ball_group, walls)

            # draw score
            score_text = FONT_30.render(str(paddle.score), True, paddle_color)
            rects += [SCREEN.blit(score_text, (10, 10))]
            #SCREEN.blit(score_text, (10, 10))

            # draw level number
            level_text = FONT_30.render("Level: "+str(paddle.level), True, paddle_color)
            rects += [SCREEN.blit(level_text, (RESOLUTION[0]-120, 10))]
            #SCREEN.blit(level_text, (RESOLUTION[0] - 120, 10))

            # draw lives
            lives_group.empty()
            for i in range(paddle.lives):
                lives_group.add(Block(width=20, height=5, position=[10 + i * 25, 5], color=paddle_color))

            # draw currently playing song
            if bg_music.state == 4:
                song_text = FONT_15.render("Music is paused", True, paddle_color)
                rects += [SCREEN.blit(song_text, (500, 5))]
                #SCREEN.blit(song_text, (500, 5))
            elif bg_music.state == 3:
                song_text = FONT_15.render(bg_music.playlist_files[bg_music.track][:-4], True, paddle_color)
                rects += [SCREEN.blit(song_text, (500, 5))]
                #SCREEN.blit(song_text, (500, 5))

            # draw sprites/objects

            lives_group.draw(SCREEN)
            paddle_group.draw(SCREEN)
            ball_group.draw(SCREEN)
            level_group.draw(SCREEN)
            mods_group.draw(SCREEN)


            """
            rects += pygame.sprite.RenderUpdates.draw(lives_group, SCREEN)
            rects += pygame.sprite.RenderUpdates.draw(paddle_group, SCREEN)
            rects += pygame.sprite.RenderUpdates.draw(ball_group, SCREEN)
            rects_lvl = pygame.sprite.RenderUpdates.draw(level_group, SCREEN)
            rects += pygame.sprite.RenderUpdates.draw(mods_group, SCREEN)

            if rects_lvl != old_rects_lvl:
                if len(old_rects_lvl) > 0:
                    for i in old_rects_lvl:
                        if i not in rects_lvl:
                            rects += [i]
                else:
                    for i in rects_lvl:
                        rects += [i]

            active_rects = rects + old_rects
            #print(len(rects), len(old_rects), len(active_rects))
            # update screen
            pygame.display.update(active_rects)
            for rect in rects:
                SCREEN.blit(bg_img, rect, rect)
            old_rects = rects[:]
            old_rects_lvl = rects_lvl[:]
            
            """

            # update screen
            pygame.display.update()
            # wait before next run
            FPS_CLOCK.tick()
            print(FPS_CLOCK)


