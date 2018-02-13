"""

Music player class file.
Defines the music player and it's functions

"""

import pygame
from pygame.locals import *
#import vlc
from os import walk
from data.utils.asset import load_music
import random


class Player:
    def __init__(self):
        # Music player information
        self.name = "Music For You"
        self.alias = "Mfy"
        self.version = 0.1

        # VLC variables
        #self.instance = vlc.Instance()  # create a new vlc instance
        #self.playlist = self.instance.media_list_new()  # create a new media list instance
        #self.player = self.instance.media_player_new()  # create a new media player instance

        # Music player states
        # 0 - Nothing special
        # 1 - Opening
        # 2 - Buffering
        # 3 - Playing
        # 4 - Paused
        # 5 - Stopped
        # 6 - Ended
        # 7 - Error
        self.state = None
        #self.states = set([0,1,2,3,4])
        self.play_all = False
        self.loop = False
        self.repeat = False
        self.shuffle = False

        # Playlist information
        self.player = pygame.mixer.music
        self.folder = "music/"  # standard folder where music is stored
        self.playlist_files = []
        self.playlist = []
        self.track = 0

    # set playback options
    def set_playback_options(self, play_all=False, loop=False, repeat=False, shuffle=False):
        self.play_all = play_all
        self.loop = loop
        self.repeat = repeat
        self.shuffle = shuffle

    # load sound to play once
    def load_sound(self, path):
        self.player.load(path)
        self.player.play()  # set media to player

    # load music from folder into a playlist
    def load_folder(self, folder="music/"):
        self.folder = folder
        for (dirpath, dirnames, filenames) in walk(self.folder):
            self.playlist_files.extend(filenames)
            break
        """
        for i in range(len(self.playlist_files)):
            media = load_music(self.playlist_files[i])
            self.playlist.append(media)  # add media to playlist
        """
    """
    change to the next track in playlist.
    if loop is true:
        will start playing from top of playlist when last song is played
    if repeat is true:
        will play the same track over and over again
    if shuffle is true:
        next track will be selected random from playlist 
    """
    def next(self):
        if self.state == 3:
            if self.player.get_busy():
                self.player.stop()
            else:
                if self.repeat:
                    self.play()  # play the next track
                elif self.shuffle:
                    while True:
                        rand = random.randint(0, len(self.playlist_files))
                        if rand != self.track:
                            self.track = rand
                            break
                    self.play()  # play the next track
                elif self.play_all:
                    if self.loop:
                        self.track = (self.track + 1) % len(self.playlist_files)
                        self.play()  # play the next track
                    else:
                        if self.track < len(self.playlist_files)-1:
                            self.track += 1
                            self.play()  # play the next track

    # change to previous track in playlist
    def previous(self):
        if self.track <= 0:
            self.track = len(self.playlist_files)
        self.track -= 1
        self.play()

    # set track to play in playlist
    def set_track(self, track=0):
        self.track = track

    # get current track in playlist
    def get_track(self):
        return self.track


    # play the current track in playlist
    def play(self):
        self.player.load(self.folder+self.playlist_files[self.track])
        self.player.play()
        self.state = 3

    # stop the current song playing
    def stop(self):
        self.player.stop()  # stop media
        self.state = 5

    # pause the current song
    def pause(self):
        self.player.pause()
        self.state = 4

    # unpause the current song. WILL CONTINUE TO PLAY FROM PLAYLIST AFTER THE SONG IS ENDED IF CHECK STATE IS RUN
    def unpause(self):
        self.player.unpause()
        self.state = 3

    # set volume between 0 - 100
    def set_volume(self, volume=0.5):
        self.player.set_volume(volume)

    # get volume
    def get_volume(self):
        return self.player.get_volume()

    # set endevent when playback stops
    def set_endevent(self, ev):
        self.player.set_endevent(ev)



