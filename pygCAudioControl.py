
# Import
import pygame as pg
from pygDataManagement import CGameAudio

# Class
class CAudioControl:
    def __init__(self):
        self.sound = 1
        self.music = 1
        self.__audio = CGameAudio()
        # pg.mixer.music.load(self.__audio.game_music)

    def play_menu_move(self):
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_menu_move)

    def play_menu_return(self):
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_menu_return)

    def play_coin_move(self):
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_coin_move)

    def play_coin_insert(self):
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_coin_insert)

    def play_win(self):
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_win)

    def play_music(self):
        self.music = 1
        # pg.mixer.music.play(-1, 0)

    def stop_music(self):
        self.music = 0
        # pg.mixer.music.stop()