
# ####################################################
# Class       : CGame
# Dependencies: pygame, pygCText, pygCMenuCursor, pygDataManagement, pygCRulesBackground
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
import pygCRulesBackground as pgRBG


# Class
class CGame:
    def __init__(self, ScreenTitle='Vier Gewinnt', DisplayWidth=800, DisplayHeight=600, DisplayMode=0):
        # Basic pygame settings
        pg.init()
        if DisplayMode == 0:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight), pg.SHOWN)

        elif DisplayMode == 1:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight), pg.FULLSCREEN)

        else:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight))

        pg.display.set_caption(ScreenTitle)
        self.GameTitle             = ScreenTitle
        self.ScreenWidth           = pg.display.get_surface().get_width()
        self.ScreenHeight          = pg.display.get_surface().get_height()
        self.BackBufferScreen      = pg.Surface((self.ScreenWidth, self.ScreenHeight))
        self.Clock                 = pg.time.Clock()

        # Data-Management-Class-Menus
        self.BasicVar              = pgDM.CBasicVar()
        self.objGameText           = pgDM.CGameText(self.BackBufferScreen)
        self.objGameImage          = pgDM.CGameImage()
        self.objGameAudio          = pgDM.CGameAudio()

        # GameMusic
        # pg.mixer.music.load(self.objGameAudio.game_music)

        # GameText-Objects --> !! FOR TESTS ONLY !!
        self.gtTEST1        = pgText.CText(self.BackBufferScreen)

        # Other Game-Objects
        self.objMenuCursor = pgMenuCursor.CMenuCursor(self.BackBufferScreen, [330, 330], 5, 30)
        self.objRulesBG = pgRBG.CRulesBackgrund(self.BackBufferScreen, [0, 0], [800, 600])


        # Info to Terminal
        print('Display Mode: {}'.format(DisplayMode))
        print('Resolution  : {}x{}'.format(self.ScreenWidth, self.ScreenHeight))

    def gLoop(self):
        while self.BasicVar.GameLoop:
            # Events
            self.__gEvents()

            # Loop-Pages
            if self.BasicVar.LoopPage == pgDM.LoopPage.title:
                self.__gTitleScreen()

            elif self.BasicVar.LoopPage == pgDM.LoopPage.menu:
                self.__gMenuScreen()

            elif self.BasicVar.LoopPage == pgDM.LoopPage.game:
                self.__gGameScreen()

            elif self.BasicVar.LoopPage == pgDM.LoopPage.rules:
                self.__gRulesScreen()

            elif self.BasicVar.LoopPage == pgDM.LoopPage.option:
                self.__gOptionScreen()

            elif self.BasicVar.LoopPage == pgDM.LoopPage.end:
                self.__gEndScreen()

            # FrontBuffer Actions
            self.FrontBufferScreen.blit(self.BackBufferScreen, (0, 0))
            pg.display.flip()
            self.Clock.tick(60)

        pg.quit()

    def __gTitleScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1
        self.BackBufferScreen.blit(self.objGameImage.img_title_screen, (150, 100))

        # Layer 2

        # Layer 3 [Text Layer]
        self.objGameText.title_bottom_info1.drawText()
        self.objGameText.title_bottom_info2.drawText()

        self.FrontBufferScreen.blit(self.BackBufferScreen, (0, 0))
        pg.display.flip()

        # Nach 5 Sekunden -> Umschaltung auf Loop-Page: Menü
        pg.time.wait(5000)
        self.BasicVar.LoopPage = pgDM.LoopPage.menu
        # pg.mixer.music.play(-1, 0)

    def __gMenuScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1
        self.BackBufferScreen.blit(self.objGameImage.img_title_screen, (150, 10))

        # Layer 2
        self.objMenuCursor.showCursor()

        # Layer 3 [Text Layer]
        self.objGameText.menu_PLvsCPU.drawText()
        self.objGameText.menu_PLvsPL.drawText()
        self.objGameText.menu_RULES.drawText()
        self.objGameText.menu_OPTION.drawText()
        self.objGameText.menu_END.drawText()

    def __gGameScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1

        # Layer 2

        # Layer 3 [Text Layer]
        self.gtTEST1.setTextName('Game Screen')
        self.gtTEST1.drawText()

    def __gRulesScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1
        self.objRulesBG.drawBackground()
        self.BackBufferScreen.blit(self.objGameImage.img_rules_01, (420, 10))

        # Layer 2

        # Layer 3 [Text Layer]
        self.objGameText.rules_TITLE.drawText()
        pg.draw.line(self.BackBufferScreen, [0, 255, 0], [40, 190], [420, 190])
        pg.draw.line(self.BackBufferScreen, [0, 255, 0], [30, 195], [400, 195])
        text_offset = 0
        for x in self.objGameText.rules_TEXT:
            self.objGameText.rules_RULES.setTextName(x)
            self.objGameText.rules_RULES.setTextPosition(50, 250 + text_offset)
            self.objGameText.rules_RULES.drawText()
            text_offset += 30

    def __gOptionScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1

        # Layer 2

        # Layer 3 [Text Layer]
        self.gtTEST1.setTextName('Option Screen')
        self.gtTEST1.drawText()

    def __gEndScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1
        self.BackBufferScreen.blit(self.objGameImage.img_title_screen, (150, 10))

        # Layer 2
        if self.BasicVar.end_yesno == 0:
            pg.draw.rect(self.BackBufferScreen, [0, 0, 255], [270, 410, 80, 30], 1)

        elif self.BasicVar.end_yesno == 1:
            pg.draw.rect(self.BackBufferScreen, [0, 0, 255], [270 + 165, 410, 80, 30], 1)

        # Layer 3 [Text Layer]
        self.objGameText.end_question.drawText()
        self.objGameText.end_yesno.drawText()

    def __gEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.BasicVar.GameLoop = False  # Spiel beenden

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Spiel beenden
                    self.BasicVar.GameLoop = False

                if self.BasicVar.LoopPage == pgDM.LoopPage.title:
                    pass

                elif self.BasicVar.LoopPage == pgDM.LoopPage.menu:

                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)
                        if self.objMenuCursor.get_cursor_state() == 0:       # Spieler vs CPU
                            self.BasicVar.LoopPage = pgDM.LoopPage.game

                        elif self.objMenuCursor.get_cursor_state() == 1:     # Spieler vs Spieler
                            self.BasicVar.LoopPage = pgDM.LoopPage.game

                        elif self.objMenuCursor.get_cursor_state() == 2:     # Spielregeln
                            self.BasicVar.LoopPage = pgDM.LoopPage.rules

                        elif self.objMenuCursor.get_cursor_state() == 3:     # Option
                            self.BasicVar.LoopPage = pgDM.LoopPage.option

                        elif self.objMenuCursor.get_cursor_state() == 4:     # Spiel beenden
                            self.BasicVar.LoopPage = pgDM.LoopPage.end

                    elif event.key == pg.K_UP:
                        if self.objMenuCursor.is_greater_min():
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                            self.objMenuCursor.set_prev_position()

                    elif event.key == pg.K_DOWN:
                        if self.objMenuCursor.is_lower_max():
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                            self.objMenuCursor.set_next_position()

                elif self.BasicVar.LoopPage == pgDM.LoopPage.game:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

                elif self.BasicVar.LoopPage == pgDM.LoopPage.rules:
                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.BasicVar.LoopPage == pgDM.LoopPage.option:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.BasicVar.LoopPage == pgDM.LoopPage.end:
                    if event.key == pg.K_RETURN:
                        pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)
                        if self.BasicVar.end_yesno == 0:
                            self.BasicVar.GameLoop = False

                        elif self.BasicVar.end_yesno == 1:
                            self.BasicVar.LoopPage = pgDM.LoopPage.menu

                    elif event.key == pg.K_LEFT:
                        if self.BasicVar.end_yesno == 1:
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                        self.BasicVar.end_yesno = 0

                    elif event.key == pg.K_RIGHT:
                        if self.BasicVar.end_yesno == 0:
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                        self.BasicVar.end_yesno = 1
