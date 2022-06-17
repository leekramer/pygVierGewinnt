
# ####################################################
# Class       : CGame
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-10
# Version     : V1.0
# ####################################################
# Description
# ===========
# Umsetzung des Spiels "Vier Gewinnt"
#
# ####################################################

# Import
import pygame as pg
import pygCText as pgText
import pygDataManagement as pgDM

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

        # Sub-Data-Class-Menus
        self.BasicVar              = pgDM.CBasicVar()
        self.objGameText           = pgDM.CGameText(self.BackBufferScreen)
        self.objGameImage          = pgDM.CGameImage()
        self.objGameAudio          = pgDM.CGameAudio()

        # GameMusic
        # pg.mixer.music.load(self.objGameAudio.game_music)

        # GameText -> Menü-Cursor
        self.gtMenu_Cursor  = pgText.CText(self.BackBufferScreen, '>', 330, 330)
        self.gtMenu_Cursor.setFontSize(25)
        self.gtMenu_Cursor.setFontBold(True)
        self.gtMenu_Cursor.setTextColor([255, 0, 0])

        # GameText-Objects --> !! FOR TESTS ONLY !!
        self.gtTEST1        = pgText.CText(self.BackBufferScreen)

        # Game-Object Defines
        # menuCursor --> Blinkender Pfeil für die Menüauswahl
        self.menuCursorTime  = 0
        self.menuCursorFreq  = 500
        self.menuCursorSwap  = False
        self.menuCursorYPos  = 330
        self.menuCursorState = 0


        # Info to Terminal
        print('Display Mode: {}'.format(DisplayMode))
        print('Resolution  : {}x{}'.format(self.ScreenWidth, self.ScreenHeight))

    def gLoop(self):
        while self.BasicVar.GameLoop:
            # Events
            self.__gEvents()

            # Loop Screens
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

        # Nach 5 Sekunden -> Umschaltung auf Menü-Loop
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
        self.__gMenuCursorAnimation()

        # Layer 3 [Text Layer]
        self.objGameText.menu_PLvsCPU.drawText()
        self.objGameText.menu_PLvsPL.drawText()
        self.objGameText.menu_RULES.drawText()
        self.objGameText.menu_OPTION.drawText()
        self.objGameText.menu_END.drawText()

    def __gMenuCursorAnimation(self):
        self.gtMenu_Cursor.drawText()
        if self.menuCursorTime == 0:
            self.menuCursorTime = pg.time.get_ticks() + self.menuCursorFreq

        elif self.menuCursorTime < pg.time.get_ticks():
            self.menuCursorTime = pg.time.get_ticks() + self.menuCursorFreq
            if self.menuCursorSwap:
                self.gtMenu_Cursor.setTextColor([0, 0, 100])
                self.menuCursorSwap = False

            elif not self.menuCursorSwap:
                self.gtMenu_Cursor.setTextColor([255, 0, 0])
                self.menuCursorSwap = True


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

        # Layer 2

        # Layer 3 [Text Layer]
        self.gtTEST1.setTextName('Rules Screen')
        self.gtTEST1.drawText()

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

        # Layer 2

        # Layer 3 [Text Layer]
        self.gtTEST1.setTextName('End Screen')
        self.gtTEST1.drawText()

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
                        if self.menuCursorState == 0:       # Spieler vs CPU
                            self.BasicVar.LoopPage = pgDM.LoopPage.game
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)

                        elif self.menuCursorState == 1:     # Spieler vs Spieler
                            self.BasicVar.LoopPage = pgDM.LoopPage.game
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)

                        elif self.menuCursorState == 2:     # Spielregeln
                            self.BasicVar.LoopPage = pgDM.LoopPage.rules
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)

                        elif self.menuCursorState == 3:     # Option
                            self.BasicVar.LoopPage = pgDM.LoopPage.option
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)

                        elif self.menuCursorState == 4:     # Spiel beenden
                            self.BasicVar.LoopPage = pgDM.LoopPage.end
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_return)


                    elif event.key == pg.K_UP:
                        if self.menuCursorYPos > 330:
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                            self.menuCursorYPos -= 30
                            self.menuCursorState -= 1
                            self.gtMenu_Cursor.setTextPosition(330, self.menuCursorYPos)

                    elif event.key == pg.K_DOWN:
                        if self.menuCursorYPos < 450:
                            pg.mixer.Sound.play(self.objGameAudio.snd_menu_move)
                            self.menuCursorYPos += 30
                            self.menuCursorState += 1
                            self.gtMenu_Cursor.setTextPosition(330, self.menuCursorYPos)
                        pass

                elif self.BasicVar.LoopPage == pgDM.LoopPage.game:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

                elif self.BasicVar.LoopPage == pgDM.LoopPage.rules:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.BasicVar.LoopPage == pgDM.LoopPage.option:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.LoopPage = pgDM.LoopPage.menu

                elif self.BasicVar.LoopPage == pgDM.LoopPage.end:
                    if event.key == pg.K_RETURN:
                        self.BasicVar.GameLoop = False

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

