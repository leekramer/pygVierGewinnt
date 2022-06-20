
# ####################################################
# Class       : CGame
# Dependencies: pygame, pygCText, pygCMenuCursor, pygDataManagement, pygCBackground
# Developer   : Lee Kramer
# Developed   : 2022-06-10
# Version     : V1.0
# ####################################################
# Description
# ===========
# Grundgerüst des Spiels
#
# ####################################################

# Import
import pygame as pg
import pygCText as pgText
import pygCMenuCursor as pgMenuCursor
import pygDataManagement as pgDM
import pygCBackground as pgBG


# Class
class CGame:
    def __init__(self, ScreenTitle='Vier Gewinnt', displayWidth=800, displayHeight=600, displayMode=0):
        # Basic pygame settings
        pg.init()
        if displayMode == 0:
            self.__FrontBufferScreen = pg.display.set_mode((displayWidth, displayHeight), pg.SHOWN)

        elif displayMode == 1:
            self.__FrontBufferScreen = pg.display.set_mode((displayWidth, displayHeight), pg.FULLSCREEN)

        else:
            self.__FrontBufferScreen = pg.display.set_mode((displayWidth, displayHeight))

        pg.display.set_caption(ScreenTitle)
        self.__GameTitle             = ScreenTitle
        self.__BackBufferScreen      = pg.Surface((displayWidth, displayHeight))
        self.__Clock                 = pg.time.Clock()

        # Data-Management-Class-Menus
        self.__BasicVar              = pgDM.CBasicVar()
        self.__objGameText           = pgDM.CGameText(self.__BackBufferScreen)
        self.__objGameImage          = pgDM.CGameImage()
        self.__objGameAudio          = pgDM.CGameAudio()

        # GameMusic
        # pg.mixer.music.load(self.objGameAudio.game_music)

        # Other Game-Objects
        self.__objMenuCursor         = pgMenuCursor.CMenuCursor(self.__BackBufferScreen, [330, 330], 5, 30)
        self.__objBG                 = pgBG.CBackgrund(self.__BackBufferScreen)

        # GameText-Objects --> !! FOR TESTS ONLY !!
        self.gtTEST1                 = pgText.CText(self.__BackBufferScreen)

        # Info to Terminal
        print('Display Mode: {}'.format(displayMode))
        print('Resolution  : {}x{}'.format(self.__BackBufferScreen.get_width(), self.__BackBufferScreen.get_height()))

    def gLoop(self):
        while self.__BasicVar.GameLoop:
            # Events
            self.__gEvents()

            # Loop-Pages
            if self.__BasicVar.LoopPage == pgDM.LoopPage.title:
                self.__gTitleScreen()

            elif self.__BasicVar.LoopPage == pgDM.LoopPage.menu:
                self.__gMenuScreen()

            elif self.__BasicVar.LoopPage == pgDM.LoopPage.game:
                self.__gGameScreen()

            elif self.__BasicVar.LoopPage == pgDM.LoopPage.rules:
                self.__gRulesScreen()

            elif self.__BasicVar.LoopPage == pgDM.LoopPage.option:
                self.__gOptionScreen()

            elif self.__BasicVar.LoopPage == pgDM.LoopPage.end:
                self.__gEndScreen()

            # FrontBuffer Actions
            self.__FrontBufferScreen.blit(self.__BackBufferScreen, (0, 0))
            pg.display.flip()
            self.__Clock.tick(60)

        pg.quit()

    def __gTitleScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1
        self.__BackBufferScreen.blit(self.__objGameImage.img_title_screen, (150, 100))

        # Layer 2

        # Layer 3 [Text Layer]
        self.__objGameText.title_bottom_info1.drawText()
        self.__objGameText.title_bottom_info2.drawText()

        self.__FrontBufferScreen.blit(self.__BackBufferScreen, (0, 0))
        pg.display.flip()

        # Nach 5 Sekunden -> Umschaltung auf Loop-Page: Menü
        pg.time.wait(5000)
        self.__BasicVar.LoopPage = pgDM.LoopPage.menu
        # pg.mixer.music.play(-1, 0)

    def __gMenuScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1
        self.__BackBufferScreen.blit(self.__objGameImage.img_title_screen, (150, 10))

        # Layer 2
        self.__objMenuCursor.showCursor()

        # Layer 3 [Text Layer]
        self.__objGameText.menu_PLvsCPU.drawText()
        self.__objGameText.menu_PLvsPL.drawText()
        self.__objGameText.menu_RULES.drawText()
        self.__objGameText.menu_OPTION.drawText()
        self.__objGameText.menu_END.drawText()

    def __gGameScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGDarkBlue()

        # Layer 1

        # Layer 2

        # Layer 3 [Text Layer]
        self.gtTEST1.setTextName('Game Screen')
        self.gtTEST1.drawText()

    def __gRulesScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1
        self.__BackBufferScreen.blit(self.__objGameImage.img_rules_01, (420, 10))

        # Layer 2

        # Layer 3 [Text Layer]
        self.__objGameText.rules_TITLE.drawText()
        pg.draw.line(self.__BackBufferScreen, [0, 255, 0], [40, 190], [420, 190])
        pg.draw.line(self.__BackBufferScreen, [0, 255, 0], [30, 195], [400, 195])
        text_offset = 0
        for x in self.__objGameText.rules_TEXT:
            self.__objGameText.rules_RULES.setTextName(x)
            self.__objGameText.rules_RULES.setTextPosition(50, 250 + text_offset)
            self.__objGameText.rules_RULES.drawText()
            text_offset += 30

    def __gOptionScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1

        # Layer 2

        # Layer 3 [Text Layer]
        self.__objGameText.option_col_pl1.drawText()
        self.__objGameText.option_col_pl2.drawText()
        self.__objGameText.option_design.drawText()
        self.__objGameText.option_music.drawText()
        self.__objGameText.option_sound.drawText()
        self.__objGameText.option_back.drawText()

    def __gEndScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1
        self.__BackBufferScreen.blit(self.__objGameImage.img_title_screen, (150, 10))

        # Layer 2
        if self.__BasicVar.end_yesno == 0:
            pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [270, 410, 80, 30], 1)

        elif self.__BasicVar.end_yesno == 1:
            pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [270 + 165, 410, 80, 30], 1)

        # Layer 3 [Text Layer]
        self.__objGameText.end_question.drawText()
        self.__objGameText.end_yesno.drawText()

    def __gEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__BasicVar.GameLoop = False  # Spiel beenden

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Spiel beenden
                    self.__BasicVar.GameLoop = False

                if self.__BasicVar.LoopPage == pgDM.LoopPage.title:
                    pass

                elif self.__BasicVar.LoopPage == pgDM.LoopPage.menu:

                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.__objGameAudio.snd_menu_return)
                        if self.__objMenuCursor.get_cursor_state() == 0:       # Spieler vs CPU
                            self.__BasicVar.LoopPage = pgDM.LoopPage.game

                        elif self.__objMenuCursor.get_cursor_state() == 1:     # Spieler vs Spieler
                            self.__BasicVar.LoopPage = pgDM.LoopPage.game

                        elif self.__objMenuCursor.get_cursor_state() == 2:     # Spielregeln
                            self.__BasicVar.LoopPage = pgDM.LoopPage.rules

                        elif self.__objMenuCursor.get_cursor_state() == 3:     # Option
                            self.__BasicVar.LoopPage = pgDM.LoopPage.option

                        elif self.__objMenuCursor.get_cursor_state() == 4:     # Spiel beenden
                            self.__BasicVar.LoopPage = pgDM.LoopPage.end

                    elif event.key == pg.K_UP:
                        if self.__objMenuCursor.is_greater_min():
                            pg.mixer.Sound.play(self.__objGameAudio.snd_menu_move)
                            self.__objMenuCursor.set_prev_position()

                    elif event.key == pg.K_DOWN:
                        if self.__objMenuCursor.is_lower_max():
                            pg.mixer.Sound.play(self.__objGameAudio.snd_menu_move)
                            self.__objMenuCursor.set_next_position()

                elif self.__BasicVar.LoopPage == pgDM.LoopPage.game:
                    if event.key == pg.K_RETURN:
                        self.__BasicVar.LoopPage = pgDM.LoopPage.menu

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

                elif self.__BasicVar.LoopPage == pgDM.LoopPage.rules:
                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.__objGameAudio.snd_menu_return)
                        self.__BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.__BasicVar.LoopPage == pgDM.LoopPage.option:
                    if event.key == pg.K_RETURN:
                        self.__BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.__BasicVar.LoopPage == pgDM.LoopPage.end:
                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.__objGameAudio.snd_menu_return)
                        if self.__BasicVar.end_yesno == 0:
                            self.__BasicVar.GameLoop = False

                        elif self.__BasicVar.end_yesno == 1:
                            self.__BasicVar.LoopPage = pgDM.LoopPage.menu

                    elif event.key == pg.K_LEFT:
                        if self.__BasicVar.end_yesno == 1:
                            pg.mixer.Sound.play(self.__objGameAudio.snd_menu_move)
                        self.__BasicVar.end_yesno = 0

                    elif event.key == pg.K_RIGHT:
                        if self.__BasicVar.end_yesno == 0:
                            pg.mixer.Sound.play(self.__objGameAudio.snd_menu_move)
                        self.__BasicVar.end_yesno = 1
