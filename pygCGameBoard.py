
# #################################################################################################
# Class       : CGameBoard
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-24
# Version     : V1.0
# #################################################################################################
# Description
# ===========
# Darstellung & Verwaltung des Spielbretts
#
# #################################################################################################

# Import
import pygame as pg
import enum
from random import randint
import pygCChip as pgChip
from pygCAudioControl import CAudioControl

# Enum
class GAME_MODE(enum.IntEnum):
    PL_VS_CPU = 0
    PL_VS_PL  = 1


# Class
class CGameBoard:
    def __init__(self, toBuffer) -> None:
        self.__BackBufferScreen = toBuffer
        self.__Audio            = CAudioControl()
        self.__chip_size        = 25
        self.__am_zug           = 1
        self.__game_mode        = 0
        self.__anim_insert_coin = False
        self.__free_coin_place  = 0
        self.__column_count     = -1
        self.__lock_key_events  = False
        self.__wait_diff        = 0
        self.__game_speed       = 50
        self.__chip_pl1         = pgChip.CChip(toBuffer)
        self.__chip_pl2         = pgChip.CChip(toBuffer)

        self.__coin_position    = 0
        self.__game_grid        = []

    def prepare_board(self, gbChipPl1: pgChip.CHIP_COLOR, gbChipPl2: pgChip.CHIP_COLOR,
                      gbChipDesign: pgChip.CHIP_DESIGN, gbGameMode: GAME_MODE) -> None:
        self.__am_zug    = randint(1, 2)
        self.__game_mode = gbGameMode

        self.__create_grid()

        self.__chip_pl1.set_chip_color(gbChipPl1)
        self.__chip_pl1.set_chip_size(self.__chip_size)
        self.__chip_pl1.set_design(gbChipDesign)

        self.__chip_pl2.set_chip_color(gbChipPl2)
        self.__chip_pl2.set_design(gbChipDesign)
        self.__chip_pl2.set_chip_size(self.__chip_size)

    def reset_board(self) -> None:
        pass

    def lock_key_events(self) -> bool:  # Sperrt Anwendereingaben solange andere Prozesse laufen
        if self.__lock_key_events:
            return True  # locked gEvents: LOOP_PAGE.GAME

        else:
            return False  # unlocked gEvents: LOOP_PAGE.GAME

    def increment_coin_position(self) -> None:
        if self.__coin_position < 6:
            self.__Audio.play_coin_move()
            self.__coin_position += 1

    def decrement_coin_position(self) -> None:
        if self.__coin_position > 0:
            self.__Audio.play_coin_move()
            self.__coin_position -= 1

    def drop_coin(self):
        if not self.__is_column_full():
            self.__palce_coin_to_grid()

    def __palce_coin_to_grid(self):
        for x in range(0, 6):
            if self.__game_grid[self.__coin_position][5 - x] == 0:
                self.__free_coin_place = 5 - x
                self.__Audio.play_coin_insert()
                self.__lock_key_events = True
                self.__anim_insert_coin = True
                return

            else:
                continue

    def __is_column_full(self) -> bool:
        for x in range(0, 6):
            if self.__game_grid[self.__coin_position][5 - x] == 0:
                return False

            else:
                continue

        return True

    def __animation_coin_insert(self):
        if self.__wait_diff <= pg.time.get_ticks():
            self.__wait_diff = pg.time.get_ticks() + self.__game_speed
            self.__column_count += 1

        if self.__column_count == self.__free_coin_place:
            self.__game_grid[self.__coin_position][self.__free_coin_place] = self.__am_zug  # Set Coin to GameGrid

            game_result = self.__grid_check()
            if game_result == 1:
                print('Spieler 1 gewinnt!')

            elif game_result == 2:
                print('Spieler 2 gewinnt!')

            elif game_result == 3:
                print('Unentschieden!')

            if self.__am_zug == 1:
                self.__am_zug = 2

            elif self.__am_zug == 2:
                self.__am_zug = 1

            self.__column_count     = -1
            self.__wait_diff        = 0
            self.__anim_insert_coin = False
            self.__lock_key_events  = False

    def __draw_board(self) -> None:
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 150], [120, 130, 580, 430], 0, 1, 20, 20, 20, 20)
        pg.draw.rect(self.__BackBufferScreen, [0, 100, 150], [120, 130, 580, 430], 3, 20)

        for x in range(0, 7):
            for y in range(0, 6):
                pg.draw.circle(self.__BackBufferScreen, [0, 0, 20], [170 + (x * 80), 170 + (y * 70)],
                               self.__chip_size + 2, 0)
                pg.draw.circle(self.__BackBufferScreen, [0, 100, 150], [170 + (x * 80), 170 + (y * 70)],
                               self.__chip_size + 2 , 3)

    def __draw_coin_grid(self):
        for x in range(0, 7):
            for y in range(0, 6):
                if self.__game_grid[x][y] == 1:
                    self.__chip_pl1.draw_chip_pos(170 + (x * 80), 170 + (y * 70))
                elif self.__game_grid[x][y] == 2:
                    self.__chip_pl2.draw_chip_pos(170 + (x * 80), 170 + (y * 70))

    def __grid_check_column(self) -> int:
        for y in range(0, 6):
            for x in range(0, 4):
                if self.__game_grid[x][5 - y] == 1 and self.__game_grid[x + 1][5 - y] == 1 and \
                   self.__game_grid[x + 2][5 - y] == 1 and self.__game_grid[x + 3][5 - y] == 1:
                    return 1

                elif self.__game_grid[x][5 - y] == 2 and self.__game_grid[x + 1][5 - y] == 2 and \
                     self.__game_grid[x + 2][5 - y] == 2 and self.__game_grid[x + 3][5 - y] == 2:
                    return 2

        return 0

    def __grid_check_row(self) -> int:
        for x in range(0, 7):
            for y in range(0, 3):
                if self.__game_grid[x][y] == 1 and self.__game_grid[x][y + 1] == 1 and \
                   self.__game_grid[x][y + 2] == 1 and self.__game_grid[x][y + 3] == 1:
                    return 1

                elif self.__game_grid[x][y] == 2 and self.__game_grid[x][y + 1] == 2 and \
                     self.__game_grid[x][y + 2] == 2 and self.__game_grid[x][y + 3] == 2:
                    return 2

        return 0

    def __grid_check_diagonal(self) -> int:
        for y in range(0, 3):
            for x in range(0, 4):
                # Direction: to right
                if self.__game_grid[x][y + 3] == 1 and self.__game_grid[x + 1][y + 2] == 1 and \
                   self.__game_grid[x + 2][y + 1] == 1 and self.__game_grid[x + 3][y] == 1:
                    return 1

                elif self.__game_grid[x][y + 3] == 2 and self.__game_grid[x + 1][y + 2] == 2 and \
                   self.__game_grid[x + 2][y + 1] == 2 and self.__game_grid[x + 3][y] == 2:
                    return 2

                # Direction_ left
                if self.__game_grid[6 - x][y + 3] == 1 and self.__game_grid[5 - x][y + 2] == 1 and \
                   self.__game_grid[4 - x][y + 1] == 1 and self.__game_grid[3 - x][y] == 1:
                    return 1

                elif self.__game_grid[6 - x][y + 3] == 2 and self.__game_grid[5 - x][y + 2] == 2 and \
                   self.__game_grid[4 - x][y + 1] == 2 and self.__game_grid[3 - x][y] == 2:
                    return 2

    def __grid_check_full(self) -> int:
        if self.__game_grid[0][0] != 0 and \
           self.__game_grid[1][0] != 0 and \
           self.__game_grid[2][0] != 0 and \
           self.__game_grid[3][0] != 0 and \
           self.__game_grid[4][0] != 0 and \
           self.__game_grid[5][0] != 0 and \
           self.__game_grid[6][0] != 0:
            return 3

        else:
            return 0

    def __grid_check(self) -> int:
        tmp_column   = self.__grid_check_column()
        tmp_row      = self.__grid_check_row()
        tmp_diagonal = self.__grid_check_diagonal()

        if tmp_column == 1 or tmp_row == 1 or tmp_diagonal == 1:
            return 1

        elif tmp_column == 2 or tmp_row == 2 or tmp_diagonal == 2:
            return 2

        elif self.__grid_check_full() == 3:
            return 3

        else:
            return 0

    def draw_gameboard(self) -> None:
        self.__draw_board()
        self.__draw_coin_grid()
        if self.__anim_insert_coin:
            self.__animation_coin_insert()
            if self.__am_zug == 1:
                self.__chip_pl1.draw_chip_pos(170 + (self.__coin_position * 80), 170 + (self.__column_count * 70))

            elif self.__am_zug == 2:
                self.__chip_pl2.draw_chip_pos(170 + (self.__coin_position * 80), 170 + (self.__column_count * 70))

        else:
            if self.__am_zug == 1:
                self.__chip_pl1.draw_chip_pos(170 + (self.__coin_position * 80), 90)

            elif self.__am_zug == 2:
                self.__chip_pl2.draw_chip_pos(170 + (self.__coin_position * 80), 90)

    def __create_grid(self) -> None:
        self.__game_grid.clear()
        for x in range(0, 7):
            tmp = []
            for y in range(0, 6):
                tmp.append(0)
            self.__game_grid.append(tmp)

    def print_grid_to_console(self) -> None:
        print('----- Game Grid -----')
        for y in range(0, 6):
            for x in range(0, 7):
                print('[' + str(self.__game_grid[x][y]) + ']', end = '')
            print('')

































