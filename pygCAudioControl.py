
# Import
import pygame as pg
from pygDataManagement import CGameAudio

# Class
class CAudioControl:
    def __init__(self) -> None:
        self.sound = 1
        self.music = 1
        self.__audio = CGameAudio()
        pg.mixer.music.load(self.__audio.game_music)
        pg.mixer.music.set_volume(0.3)

    def play_menu_move(self) -> None:
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_menu_move)

    def play_menu_return(self) -> None:
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_menu_return)

    def play_coin_move(self) -> None:
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_coin_move)

    def play_coin_insert(self) -> None:
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_coin_insert)

    def play_win(self) -> None:
        if self.sound == 1:
            pg.mixer.Sound.play(self.__audio.snd_win)

    def play_music(self) -> None:
        self.music = 1
        pg.mixer.music.play(-1, 0)

    def stop_music(self) -> None:
        self.music = 0
        pg.mixer.music.stop()