
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


# Defines
LOOP_TITLE_SCREEN  = 0
LOOP_MENU_SCREEN   = 1
LOOP_GAME_SCREEN   = 2
LOOP_RULES_SCREEN  = 3
LOOP_OPTION_SCREEN = 4
LOOP_END_SCREEN    = 5


# Class
class CGame:
    def __init__(self, ScreenTitle='Vier Gewinnt', DisplayWidth=800, DisplayHeight=600, DisplayMode=0):
        # System Defines
        pg.init()
        if DisplayMode == 0:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight), pg.SHOWN)

        elif DisplayMode == 1:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight), pg.FULLSCREEN)

        else:
            self.FrontBufferScreen = pg.display.set_mode((DisplayWidth, DisplayHeight))

        pg.display.set_caption(ScreenTitle)
        self.GameTitle = ScreenTitle
        self.ScreenWidth = pg.display.get_surface().get_width()
        self.ScreenHeight = pg.display.get_surface().get_height()
        self.BackBufferScreen = pg.Surface((self.ScreenWidth, self.ScreenHeight))
        self.Clock = pg.time.Clock()


        # GameText-Objects --> Title-Screen
        # GameText: InfoLine1
        self.gtInfoLine1 = pgText.CText(
            self.BackBufferScreen, 'Producer: Lee Kramer  -  Produced: 2022-06-10  -  Version: 1.0', 180, 550)
        self.gtInfoLine1.setFontSize(18)
        self.gtInfoLine1.setTextColor([80, 80, 0])

        # GameText: InfoLine2
        self.gtInfoLine2 = pgText.CText(
            self.BackBufferScreen, 'Made with Python 3.10 & PyGame 2.1.0', 250, 570)
        self.gtInfoLine2.setFontSize(18)
        self.gtInfoLine2.setTextColor([80, 80, 0])


        # GameText-Objects --> Menu-Screen
        gtMenuOffset        = 30
        menuFontSize        = 25
        menuTextColor       = [160, 160, 160]

        self.gtMenu_PLvsCPU = pgText.CText(self.BackBufferScreen, 'Spieler vs CPU', 350, 300 + 1 * gtMenuOffset)
        self.gtMenu_PLvsCPU.setFontSize(menuFontSize)
        self.gtMenu_PLvsCPU.setTextColor(menuTextColor)

        self.gtMenu_PLvsPL  = pgText.CText(self.BackBufferScreen, 'Spieler vs Spieler', 350, 300 + 2 * gtMenuOffset)
        self.gtMenu_PLvsPL.setFontSize(menuFontSize)
        self.gtMenu_PLvsPL.setTextColor(menuTextColor)

        self.gtMenu_RULES   = pgText.CText(self.BackBufferScreen, 'Spielregeln', 350, 300 + 3 * gtMenuOffset)
        self.gtMenu_RULES.setFontSize(menuFontSize)
        self.gtMenu_RULES.setTextColor(menuTextColor)

        self.gtMenu_OPTION  = pgText.CText(self.BackBufferScreen, 'Option', 350, 300 + 4 * gtMenuOffset)
        self.gtMenu_OPTION.setFontSize(menuFontSize)
        self.gtMenu_OPTION.setTextColor(menuTextColor)

        self.gtMenu_END     = pgText.CText(self.BackBufferScreen, 'Spiel beenden', 350, 300 + 5 * gtMenuOffset)
        self.gtMenu_END.setFontSize(menuFontSize)
        self.gtMenu_END.setTextColor(menuTextColor)

        self.gtMenu_Cursor  = pgText.CText(self.BackBufferScreen, '>', 330, 330)
        self.gtMenu_Cursor.setFontSize(menuFontSize)
        self.gtMenu_Cursor.setFontBold(True)
        self.gtMenu_Cursor.setTextColor([255, 0, 0])

        # GameText-Objects --> !! FOR TESTS ONLY !!
        self.gtTEST1        = pgText.CText(self.BackBufferScreen)


        # GameImage-Objects
        self.giTitle = pg.image.load('./graphic/titelbild.png')

        # GameAudio-Objects --> Music
        # pg.mixer.music.load('')
        # pg.mixer.music.play(-1, 0)

        # GameAudio-Objects --> Sounds
        self.gsMenuMove      = pg.mixer.Sound('./audio/menu_move.mp3')
        self.gsMenuReturn    = pg.mixer.Sound('./audio/menu_return.mp3')
        self.gsCoinInsert    = pg.mixer.Sound('./audio/coin_insert.mp3')
        self.gsCoinMove      = pg.mixer.Sound('./audio/coin_move.mp3')
        self.gsWin           = pg.mixer.Sound('./audio/win.mp3')

        # Game Defines
        self.GameLoop        = True
        self.GameBreak       = False
        self.LoopPage        = LOOP_TITLE_SCREEN  # LOOP_MENU_SCREEN  # LOOP_TITLE_SCREEN
        self.TitleScreen_ON  = True
        self.Music_ON        = False
        self.Sound_ON        = False

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
        while self.GameLoop:
            # Events
            self.__gEvents()

            # Loop Screens
            if self.LoopPage == LOOP_TITLE_SCREEN:
                self.__gTitleScreen()

            elif self.LoopPage == LOOP_MENU_SCREEN:
                self.__gMenuScreen()

            elif self.LoopPage == LOOP_GAME_SCREEN:
                self.__gGameScreen()

            elif self.LoopPage == LOOP_RULES_SCREEN:
                self.__gRulesScreen()

            elif self.LoopPage == LOOP_OPTION_SCREEN:
                self.__gOptionScreen()

            elif self.LoopPage == LOOP_END_SCREEN:
                self.__gEndScreen()

            # FrontBuffer Actions
            self.FrontBufferScreen.blit(self.BackBufferScreen, (0, 0))
            pg.display.flip()
            self.Clock.tick(60)

        pg.quit()

    def __gTitleScreen(self):
        if self.TitleScreen_ON:
            # BackBuffer Actions
            # Layer 0 [Foundation Layer]
            self.BackBufferScreen.fill((0, 0, 0))

            # Layer 1
            self.BackBufferScreen.blit(self.giTitle, (150, 100))

            # Layer 2

            # Layer 3 [Text Layer]
            self.gtInfoLine1.drawText()
            self.gtInfoLine2.drawText()

            self.TitleScreen_ON = False

        # Nach 5 Sekunden -> Umschaltung auf Menü-Loop
        elif not self.TitleScreen_ON:
            pg.time.wait(5000)
            self.LoopPage = LOOP_MENU_SCREEN

    def __gMenuScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.BackBufferScreen.fill((0, 0, 0))

        # Layer 1
        self.BackBufferScreen.blit(self.giTitle, (150, 10))

        # Layer 2
        self.__gMenuCursorAnimation()

        # Layer 3 [Text Layer]
        self.gtMenu_PLvsCPU.drawText()
        self.gtMenu_PLvsPL.drawText()
        self.gtMenu_RULES.drawText()
        self.gtMenu_OPTION.drawText()
        self.gtMenu_END.drawText()


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
                self.GameLoop = False  # Spiel beenden

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Spiel beenden
                    self.GameLoop = False

                if self.LoopPage == LOOP_TITLE_SCREEN:
                    pass

                elif self.LoopPage == LOOP_MENU_SCREEN:
                    if event.key == pg.K_RETURN:
                        if self.menuCursorState == 0:       # Spieler vs CPU
                            pg.mixer.Sound.play(self.gsMenuReturn)
                            self.LoopPage        = LOOP_GAME_SCREEN

                        elif self.menuCursorState == 1:     # Spieler vs Spieler
                            self.LoopPage        = LOOP_GAME_SCREEN
                            pg.mixer.Sound.play(self.gsMenuReturn)

                        elif self.menuCursorState == 2:     # Spielregeln
                            self.LoopPage        = LOOP_RULES_SCREEN
                            pg.mixer.Sound.play(self.gsMenuReturn)

                        elif self.menuCursorState == 3:     # Option
                            self.LoopPage        = LOOP_OPTION_SCREEN
                            pg.mixer.Sound.play(self.gsMenuReturn)

                        elif self.menuCursorState == 4:     # Spiel beenden
                            self.LoopPage        = LOOP_END_SCREEN
                            pg.mixer.Sound.play(self.gsMenuReturn)


                    elif event.key == pg.K_UP:
                        if self.menuCursorYPos > 330:
                            pg.mixer.Sound.play(self.gsMenuMove)
                            self.menuCursorYPos -= 30
                            self.menuCursorState -= 1
                            self.gtMenu_Cursor.setTextPosition(330, self.menuCursorYPos)

                    elif event.key == pg.K_DOWN:
                        if self.menuCursorYPos < 450:
                            pg.mixer.Sound.play(self.gsMenuMove)
                            self.menuCursorYPos += 30
                            self.menuCursorState += 1
                            self.gtMenu_Cursor.setTextPosition(330, self.menuCursorYPos)
                        pass

                elif self.LoopPage == LOOP_GAME_SCREEN:
                    if event.key == pg.K_RETURN:
                        self.LoopPage = LOOP_MENU_SCREEN

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

                elif self.LoopPage == LOOP_RULES_SCREEN:
                    if event.key == pg.K_RETURN:
                        self.LoopPage = LOOP_MENU_SCREEN

                elif self.LoopPage == LOOP_OPTION_SCREEN:
                    if event.key == pg.K_RETURN:
                        self.LoopPage = LOOP_MENU_SCREEN

                elif self.LoopPage == LOOP_END_SCREEN:
                    if event.key == pg.K_RETURN:
                        self.GameLoop = False

                    elif event.key == pg.K_LEFT:
                        pass

                    elif event.key == pg.K_RIGHT:
                        pass

