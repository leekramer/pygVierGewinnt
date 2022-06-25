
# #################################################################################################
# Class       : CGame
# Dependencies: pygame, pygCMenuCursor, pygDataManagement, pygCBackground
# Developer   : Lee Kramer
# Developed   : 2022-06-10
# Version     : V1.0
# #################################################################################################
# Description
# ===========
# Grundgerüst des Spiels
#
# #################################################################################################

# Import
import pygame as pg
import pygCMenuCursor as pgMenuCursor
import pygDataManagement as pgDM
import pygCAudioControl as pgAudio
import pygCBackground as pgBG
import pygCChip as pgChip
import pygCGameBoard as pgBoard


# Class
class CGame:
    def __init__(self):
        # Basic pygame settings
        self.ScreenTitle             = 'Vier Gewinnt'
        self.displayWidth            = 800
        self.displayHeight           = 600
        self.displayMode             = 0

        pg.init()

        if self.displayMode == 0:
            self.__FrontBufferScreen = pg.display.set_mode((self.displayWidth, self.displayHeight), pg.SHOWN)

        elif self.displayMode == 1:
            self.__FrontBufferScreen = pg.display.set_mode((self.displayWidth, self.displayHeight), pg.FULLSCREEN)

        else:
            self.__FrontBufferScreen = pg.display.set_mode((self.displayWidth, self.displayHeight))

        self.__BackBufferScreen      = pg.Surface((self.displayWidth, self.displayHeight))
        self.__Clock                 = pg.time.Clock()

        # Data-Management-Class-Menus
        self.__BasicVar              = pgDM.CBasicVar()
        self.__objGameText           = pgDM.CGameText(self.__BackBufferScreen)
        self.__objGameImage          = pgDM.CGameImage()

        pg.display.set_caption(self.ScreenTitle)
        pg.display.set_icon(self.__objGameImage.icon)

        # GameAudio
        self.__Audio                 = pgAudio.CAudioControl()

        # Other Game-Objects
        self.__objMenuCursor         = pgMenuCursor.CMenuCursor(self.__BackBufferScreen, [330, 330], 5, 30)
        self.__objBG                 = pgBG.CBackgrund(self.__BackBufferScreen)
        self.__objChip               = pgChip.CChip(self.__BackBufferScreen, 0, 0)
        self.__objBoard              = pgBoard.CGameBoard(self.__BackBufferScreen)

        # Info to Terminal
        print('Display Mode: {}'.format(self.displayMode))
        print('Resolution  : {}x{}'.format(self.__BackBufferScreen.get_width(), self.__BackBufferScreen.get_height()))

    def gLoop(self):
        while self.__BasicVar.GameLoop:
            # Events
            self.__gEvents()

            # Loop-Pages
            if self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.TITLE:
                self.__gTitleScreen()

            elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.MENU:
                self.__gMenuScreen()

            elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.GAME:
                self.__gGameScreen()

            elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.RULES:
                self.__gRulesScreen()

            elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.OPTION:
                self.__gOptionScreen()

            elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.END:
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
        self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.MENU
        self.__Audio.play_music()

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
        self.__objBoard.draw_gameboard()

        # Layer 2

        # Layer 3 [Text Layer]

    def __gRulesScreen(self):
        # BackBuffer Actions
        # Layer 0 [Foundation Layer]
        self.__objBG.drawBGGridballs()

        # Layer 1
        self.__BackBufferScreen.blit(self.__objGameImage.img_rules_01, (420, 10))

        # Layer 2

        # Layer 3 [Text Layer]
        self.__objGameText.rules_TITLE.drawText()
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [40, 190], [420, 190])
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [30, 195], [400, 195])
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
        for i in range(0, 4):
            self.__objChip.draw_chip(295 + (i * 70), 210, i, self.__BasicVar.ChipDesign)
            self.__objChip.draw_chip(295 + (i * 70), 300, i, self.__BasicVar.ChipDesign)
            self.__objChip.draw_chip(295 + (i * 70), 390, 4, i)

        # Layer 2

        # Layer 3 [Text Layer]
        self.__objGameText.option_title.drawText()

        # Underlines Option-Title
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [250, 133], [600, 133])
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [230, 138], [580, 138])

        # Lines
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [250, 493], [600, 493])
        pg.draw.line(self.__BackBufferScreen, [0, 150, 0], [230, 498], [580, 498])

        self.__objGameText.option_col_pl1.drawText()
        self.__objGameText.option_col_pl2.drawText()
        self.__objGameText.option_design.drawText()

        self.__objGameText.option_music.drawText()
        self.__objGameText.option_music_an.drawText()
        self.__objGameText.option_music_aus.drawText()

        self.__objGameText.option_sound.drawText()
        self.__objGameText.option_sound_an.drawText()
        self.__objGameText.option_sound_aus.drawText()

        self.__objGameText.option_back.drawText()

        pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [270 + (self.__BasicVar.Pl1_Color * 70), 185, 50, 50], 1)
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [270 + (self.__BasicVar.Pl2_Color * 70), 275, 50, 50], 1)
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [270 + (self.__BasicVar.ChipDesign * 70), 365, 50, 50], 1)
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [350 + (self.__Audio.music * 70), 420, 50, 28], 1)
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 255], [350 + (self.__Audio.sound * 70), 450, 50, 28], 1)

        if self.__BasicVar.option_menu == 0:
            self.__objGameText.option_col_pl1.setTextColor([0, 0, 255])
            self.__objGameText.option_col_pl2.setTextColor([160, 160, 160])
            self.__objGameText.option_design.setTextColor([160, 160, 160])
            self.__objGameText.option_music.setTextColor([160, 160, 160])
            self.__objGameText.option_sound.setTextColor([160, 160, 160])
            self.__objGameText.option_back.setTextColor([160, 160, 160])

        elif self.__BasicVar.option_menu == 1:
            self.__objGameText.option_col_pl1.setTextColor([160, 160, 160])
            self.__objGameText.option_col_pl2.setTextColor([0, 0, 255])
            self.__objGameText.option_design.setTextColor([160, 160, 160])
            self.__objGameText.option_music.setTextColor([160, 160, 160])
            self.__objGameText.option_sound.setTextColor([160, 160, 160])
            self.__objGameText.option_back.setTextColor([160, 160, 160])

        elif self.__BasicVar.option_menu == 2:
            self.__objGameText.option_col_pl1.setTextColor([160, 160, 160])
            self.__objGameText.option_col_pl2.setTextColor([160, 160, 160])
            self.__objGameText.option_design.setTextColor([0, 0, 255])
            self.__objGameText.option_music.setTextColor([160, 160, 160])
            self.__objGameText.option_sound.setTextColor([160, 160, 160])
            self.__objGameText.option_back.setTextColor([160, 160, 160])

        elif self.__BasicVar.option_menu == 3:
            self.__objGameText.option_col_pl1.setTextColor([160, 160, 160])
            self.__objGameText.option_col_pl2.setTextColor([160, 160, 160])
            self.__objGameText.option_design.setTextColor([160, 160, 160])
            self.__objGameText.option_music.setTextColor([0, 0, 255])
            self.__objGameText.option_sound.setTextColor([160, 160, 160])
            self.__objGameText.option_back.setTextColor([160, 160, 160])

        elif self.__BasicVar.option_menu == 4:
            self.__objGameText.option_col_pl1.setTextColor([160, 160, 160])
            self.__objGameText.option_col_pl2.setTextColor([160, 160, 160])
            self.__objGameText.option_design.setTextColor([160, 160, 160])
            self.__objGameText.option_music.setTextColor([160, 160, 160])
            self.__objGameText.option_sound.setTextColor([0, 0, 255])
            self.__objGameText.option_back.setTextColor([160, 160, 160])

        elif self.__BasicVar.option_menu == 5:
            self.__objGameText.option_col_pl1.setTextColor([160, 160, 160])
            self.__objGameText.option_col_pl2.setTextColor([160, 160, 160])
            self.__objGameText.option_design.setTextColor([160, 160, 160])
            self.__objGameText.option_music.setTextColor([160, 160, 160])
            self.__objGameText.option_sound.setTextColor([160, 160, 160])
            self.__objGameText.option_back.setTextColor([0, 0, 255])

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
                    self.__BasicVar.option_menu = 0

                if self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.TITLE:                             # >>> LOOP_PAGE: Title
                    pass

                elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.MENU:                            # >>> LOOP_PAGE: Menu

                    if event.key == pg.K_RETURN:
                        self.__Audio.play_menu_return()

                        if self.__objMenuCursor.get_cursor_state() == 0:    # Spieler vs CPU
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.GAME
                            self.__objBoard.prepare_board(self.__BasicVar.Pl1_Color, self.__BasicVar.Pl2_Color,
                                                          self.__BasicVar.ChipDesign, pgBoard.GAME_MODE.PL_VS_CPU)

                        elif self.__objMenuCursor.get_cursor_state() == 1:  # Spieler vs Spieler
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.GAME
                            self.__objBoard.prepare_board(self.__BasicVar.Pl1_Color, self.__BasicVar.Pl2_Color,
                                                          self.__BasicVar.ChipDesign, pgBoard.GAME_MODE.PL_VS_PL)

                        elif self.__objMenuCursor.get_cursor_state() == 2:  # Spielregeln
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.RULES

                        elif self.__objMenuCursor.get_cursor_state() == 3:  # Option
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.OPTION

                        elif self.__objMenuCursor.get_cursor_state() == 4:  # Spiel beenden
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.END

                    elif event.key == pg.K_UP:
                        if self.__objMenuCursor.is_greater_min():
                            self.__objMenuCursor.set_prev_position()
                            self.__Audio.play_menu_move()

                    elif event.key == pg.K_DOWN:
                        if self.__objMenuCursor.is_lower_max():
                            self.__objMenuCursor.set_next_position()
                            self.__Audio.play_menu_move()

                elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.GAME:                            # >>> LOOP_PAGE: Game
                    if self.__objBoard.game_result() != 0:
                        if event.key == pg.K_RETURN:
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.MENU
                            self.__Audio.play_menu_return()

                    if not self.__objBoard.lock_key_events():
                        if event.key == pg.K_RETURN:
                            self.__objBoard.drop_coin()

                        elif event.key == pg.K_g:
                            self.__objBoard.print_grid_to_console()

                        elif event.key == pg.K_LEFT:
                            self.__objBoard.decrement_coin_position()

                        elif event.key == pg.K_RIGHT:
                            self.__objBoard.increment_coin_position()

                elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.RULES:                           # >>> LOOP_PAGE: Rules
                    if event.key == pg.K_RETURN:
                        self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.MENU
                        self.__Audio.play_menu_return()

                elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.OPTION:                          # >>> LOOP_PAGE: Option
                    if event.key == pg.K_RETURN:
                        if self.__BasicVar.option_menu == 5:
                            self.__BasicVar.option_menu = 0
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.MENU
                            self.__Audio.play_menu_return()

                    elif event.key == pg.K_UP:
                        if self.__BasicVar.option_menu > 0:
                            self.__BasicVar.option_menu -= 1
                            self.__Audio.play_menu_move()

                    elif event.key == pg.K_DOWN:
                        if self.__BasicVar.option_menu < 5:
                            self.__BasicVar.option_menu += 1
                            self.__Audio.play_menu_move()

                    elif event.key == pg.K_LEFT:
                        if self.__BasicVar.option_menu == 0:    # Chipfarbe Spieler 1
                            if self.__BasicVar.Pl1_Color > 0:
                                self.__BasicVar.Pl1_Color -= 1
                                self.__Audio.play_menu_move()

                                if self.__BasicVar.Pl1_Color == self.__BasicVar.Pl2_Color:  # Kollisionskontrolle
                                    if self.__BasicVar.Pl2_Color > 0:
                                        self.__BasicVar.Pl1_Color -= 1

                                    else:
                                        self.__BasicVar.Pl1_Color += 1

                        elif self.__BasicVar.option_menu == 1:  # Chipfarbe CPU oder Spieler 2
                            if self.__BasicVar.Pl2_Color > 0:
                                self.__BasicVar.Pl2_Color -= 1
                                self.__Audio.play_menu_move()

                                if self.__BasicVar.Pl2_Color == self.__BasicVar.Pl1_Color:  # Kollisionskontrolle
                                    if self.__BasicVar.Pl1_Color > 0:
                                        self.__BasicVar.Pl2_Color -= 1

                                    else:
                                        self.__BasicVar.Pl2_Color += 1

                        elif self.__BasicVar.option_menu == 2:  # Chipdesign
                            if self.__BasicVar.ChipDesign > 0:
                                self.__BasicVar.ChipDesign -= 1
                                self.__Audio.play_menu_move()

                        elif self.__BasicVar.option_menu == 3:  # Musik
                            if self.__Audio.music > 0:
                                self.__Audio.music -= 1
                                self.__Audio.play_menu_move()
                                self.__Audio.stop_music()

                        elif self.__BasicVar.option_menu == 4:  # Sound
                            if self.__Audio.sound > 0:
                                self.__Audio.sound -= 1
                                self.__Audio.play_menu_move()

                    elif event.key == pg.K_RIGHT:
                        if self.__BasicVar.option_menu == 0:    # Chipfarbe Spieler 1
                            if self.__BasicVar.Pl1_Color < 3:
                                self.__BasicVar.Pl1_Color += 1
                                self.__Audio.play_menu_move()

                                if self.__BasicVar.Pl1_Color == self.__BasicVar.Pl2_Color:  # Kollisionskontrolle
                                    if self.__BasicVar.Pl2_Color < 3:
                                        self.__BasicVar.Pl1_Color += 1

                                    else:
                                        self.__BasicVar.Pl1_Color -= 1

                        elif self.__BasicVar.option_menu == 1:  # Chipfarbe CPU oder Spieler 2
                            if self.__BasicVar.Pl2_Color < 3:
                                self.__BasicVar.Pl2_Color += 1
                                self.__Audio.play_menu_move()

                                if self.__BasicVar.Pl2_Color == self.__BasicVar.Pl1_Color:  # Kollisionskontrolle
                                    if self.__BasicVar.Pl1_Color < 3:
                                        self.__BasicVar.Pl2_Color += 1

                                    else:
                                        self.__BasicVar.Pl2_Color -= 1

                        elif self.__BasicVar.option_menu == 2:  # Chipdesign
                            if self.__BasicVar.ChipDesign < 3:
                                self.__BasicVar.ChipDesign += 1
                                self.__Audio.play_menu_move()

                        elif self.__BasicVar.option_menu == 3:  # Musik
                            if self.__Audio.music < 1:
                                self.__Audio.play_menu_move()

                                self.__Audio.music += 1
                                self.__Audio.play_music()

                        elif self.__BasicVar.option_menu == 4:  # Sound
                            if self.__Audio.sound < 1:
                                self.__Audio.play_menu_move()
                                self.__Audio.sound += 1


                elif self.__BasicVar.LoopPage == pgDM.LOOP_PAGE.END:                             # >>> LOOP_PAGE: End
                    if event.key == pg.K_RETURN:
                        self.__Audio.play_menu_return()

                        if self.__BasicVar.end_yesno == 0:  # Spiel beenden? -> Ja
                            self.__BasicVar.GameLoop = False
                            self.__Audio.stop_music()

                        elif self.__BasicVar.end_yesno == 1:  # Spiel beenden? -> Nein
                            self.__BasicVar.LoopPage = pgDM.LOOP_PAGE.MENU

                    elif event.key == pg.K_LEFT:
                        if self.__BasicVar.end_yesno == 1:
                            self.__Audio.play_menu_move()

                        self.__BasicVar.end_yesno = 0

                    elif event.key == pg.K_RIGHT:
                        if self.__BasicVar.end_yesno == 0:
                            self.__Audio.play_menu_move()

                        self.__BasicVar.end_yesno = 1
