
# #################################################################################################
# Class       : CBasicVar, CGameText, CGameImage, CGameAudio
# Dependencies: pygame, pygCText, enum
# Developer   : Lee Kramer
# Developed   : 2022-06-17
# Version     : V1.0
# #################################################################################################
# Description
# ===========
# Daten-Klassen-Struktur zum Organisieren der Daten
#
# #################################################################################################

# Import
import pygame as pg
from pygcTextV20220610 import cText
import enum


# Enum
class LOOP_PAGE(enum.IntEnum):
    TITLE     = 0
    MENU      = 1
    GAME      = 2
    RULES     = 3
    OPTION    = 4
    END       = 5

# Class
class CBasicVar:
    def __init__(self):
        self.GameLoop    = True
        self.LoopPage    = LOOP_PAGE.TITLE
        self.Pl1_Color   = 0
        self.Pl2_Color   = 1
        self.ChipDesign  = 0

        self.end_yesno   = 1
        self.option_menu = 0


class CGameText:
    def __init__(self, toBuffer):
        # GameText -> Title-Screen
        self.title_bottom_info1 = cText(toBuffer, '', 180, 550)
        self.title_bottom_info1.setTextName('Producer: Lee Kramer  -  Produced: 2022-06-10  -  Version: 1.0')
        self.title_bottom_info1.setFontSize(18)
        self.title_bottom_info1.setTextColor([80, 80, 0])

        self.title_bottom_info2 = cText(toBuffer, 'Made with Python 3.10 & PyGame 2.1.0', 250, 570,
                                              self.title_bottom_info1.extractAttributes())

        # GameText -> Menu-Screen
        self.menu_PLvsCPU = cText(toBuffer, 'Spieler vs CPU', 350, 300 + 1 * 30)
        self.menu_PLvsCPU.setFontSize(25)
        self.menu_PLvsCPU.setTextColor([160, 160, 160])

        self.menu_PLvsPL = cText(toBuffer, 'Spieler vs Spieler', 350, 300 + 2 * 30,
                                       self.menu_PLvsCPU.extractAttributes())

        self.menu_RULES  = cText(toBuffer, 'Spielregeln', 350, 300 + 3 * 30,
                                       self.menu_PLvsCPU.extractAttributes())

        self.menu_OPTION = cText(toBuffer, 'Option', 350, 300 + 4 * 30,
                                       self.menu_PLvsCPU.extractAttributes())

        self.menu_END = cText(toBuffer, 'Spiel beenden', 350, 300 + 5 * 30,
                                    self.menu_PLvsCPU.extractAttributes())

        # GameText -> Game-Screen


        # GameText -> Rules-Screen
        self.rules_TITLE = cText(toBuffer, 'Regeln für Vier Gewinnt', 50, 150)
        self.rules_TITLE.setFontType('Segoe UI')
        self.rules_TITLE.setFontBold(True)
        self.rules_TITLE.setFontSize(30)
        self.rules_TITLE.setTextColor([0, 255, 0])

        self.rules_RULES = cText(toBuffer, '', 50, 250)
        self.rules_RULES.setFontType('Segoe UI')
        self.rules_RULES.setTextColor([0, 255, 0])

        self.rules_TEXT = ['Das Spiel wird auf einem senkrecht',
                           'stehenden hohlen Spielbrett gespielt, in das die',
                           'Spieler abwechselnd ihre Spielsteine fallen lassen. Das Spielbrett',
                           'besteht aus sieben Spalten (senkrecht) und sechs Reihen',
                           '(waagerecht). Jeder Spieler besitzt 21 gleichfarbige Spielsteine. Wenn ein Spieler',
                           'einen Spielstein in eine Spalte fallen lässt, besetzt dieser den untersten freien Platz',
                           'der Spalte. Gewinner ist der Spieler, der es als erster schafft, vier oder mehr',
                           'seiner Spielsteine waagerecht, senkrecht oder diagonal in eine Linie zu bringen. Das',
                           'Spiel endet unentschieden, wenn das Spielbrett komplett gefüllt ist, ohne dass ein',
                           'Spieler eine Viererlinie gebildet hat.']

        # GameText -> Option-Screen
        self.option_title = cText(toBuffer, 'Option', 270, 100)
        self.option_title.setFontBold(True)
        self.option_title.setFontSize(30)
        self.option_title.setTextColor([0, 255, 0])

        self.option_col_pl1 = cText(toBuffer, 'Chipfarbe Spieler 1', 270, 150)
        self.option_col_pl1.setFontSize(25)
        self.option_col_pl1.setTextColor([160, 160, 160])

        self.option_col_pl2 = cText(toBuffer, 'Chipfarbe CPU oder Spieler 2', 270, 240,
                                          self.option_col_pl1.extractAttributes())

        self.option_design = cText(toBuffer, 'Chipdesign', 270, 330,
                                         self.option_col_pl1.extractAttributes())

        self.option_music = cText(toBuffer, 'Musik', 270, 420,
                                        self.option_col_pl1.extractAttributes())

        self.option_music_an = cText(toBuffer, 'AUS', 355, 420)
        self.option_music_an.setFontSize(25)
        self.option_music_an.setTextColor([255, 0, 0])

        self.option_music_aus = cText(toBuffer, 'AN', 430, 420)
        self.option_music_aus.setFontSize(25)
        self.option_music_aus.setTextColor([0, 255, 0])

        self.option_sound = cText(toBuffer, 'Sound', 270, 450,
                                        self.option_col_pl1.extractAttributes())

        self.option_sound_an = cText(toBuffer, 'AUS', 355, 450)
        self.option_sound_an.setFontSize(25)
        self.option_sound_an.setTextColor([255, 0, 0])

        self.option_sound_aus = cText(toBuffer, 'AN', 430, 450)
        self.option_sound_aus.setFontSize(25)
        self.option_sound_aus.setTextColor([0, 255, 0])

        self.option_back = cText(toBuffer, 'Zurück', 270, 510,
                                       self.option_col_pl1.extractAttributes())

        # GameText -> End-Screen
        self.end_question = cText(toBuffer, 'Möchtest du das Spiel beenden?', 250, 360)
        self.end_question.setFontSize(25)
        self.end_question.setTextColor([255, 0, 0])

        self.end_yesno = cText(toBuffer, 'Ja                      Nein', 300, 410,
                                     self.end_question.extractAttributes())

class CGameImage:
    def __init__(self):
        self.img_title_screen = pg.image.load('./graphic/vg_title.png')
        self.img_rules_01     = pg.image.load('./graphic/vg_01.png')
        self.icon             = pg.image.load('./graphic/vg_icon.png')


class CGameAudio:
    def __init__(self):
        # Game Sounds
        self.snd_menu_move    = pg.mixer.Sound('./audio/menu_move.mp3')
        self.snd_menu_return  = pg.mixer.Sound('./audio/menu_return.mp3')
        self.snd_coin_move    = pg.mixer.Sound('./audio/coin_move.mp3')
        self.snd_coin_insert  = pg.mixer.Sound('./audio/coin_insert.mp3')
        self.snd_win          = pg.mixer.Sound('./audio/win.mp3')

        # Game Music
        self.game_music       = './audio/music.mp3'

