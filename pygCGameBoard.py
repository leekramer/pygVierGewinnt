
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
from pygCText import CText


# Enum
class GAME_MODE(enum.IntEnum):
    PL_VS_CPU = 0
    PL_VS_PL  = 1

class KEY_EVENTS(enum.IntEnum):
    LOCKED    = True
    UNLOCKED  = False

class DIFFICULTY(enum.IntEnum):
    STUPID    = 0
    NORMAL    = 1
    DIFFICULT = 2

# Class
class CGameBoard:
    def __init__(self, toBuffer) -> None:
        self.__BackBufferScreen  = toBuffer
        self.__Audio             = CAudioControl()
        self.__chip_size         = 25
        self.__am_zug            = 1
        self.__game_grid         = []
        self.__game_mode         = GAME_MODE.PL_VS_CPU
        self.__game_speed        = 50
        self.__game_result       = 0
        self.__anim_insert_coin  = False
        self.__free_coin_place   = 0
        self.__coin_position     = 0
        self.__column_count      = -1
        self.__lock_key_events   = KEY_EVENTS.UNLOCKED
        self.__wait_diff         = 0
        self.__cpu_difficulty    = DIFFICULTY.NORMAL
        self.__cpu_drop_position = 0
        self.__cpu_access_ones   = True
        self.__chip_pl1          = pgChip.CChip(toBuffer)
        self.__chip_pl2          = pgChip.CChip(toBuffer)

        self.__gtWin             = CText(self.__BackBufferScreen, 'Win', 220, 230)
        self.__gtWin.setFontSize(30)
        self.__gtWin.setFontType('Segoe UI')
        self.__gtWin.setFontBold(True)
        self.__gtWin.setTextColor([0, 255, 0])

        self.__gtWeiter          = CText(self.__BackBufferScreen, 'Weiter mit "Return"-Taste ...', 310, 290)
        self.__gtWeiter.setTextColor([120, 120, 0])


    def prepare_board(self, gbChipPl1: pgChip.CHIP_COLOR, gbChipPl2: pgChip.CHIP_COLOR,
                      gbChipDesign: pgChip.CHIP_DESIGN, gbGameMode: GAME_MODE) -> None:
        self.__am_zug          = randint(1, 2)
        self.__game_mode       = gbGameMode
        self.__game_result     = 0
        self.__lock_key_events = KEY_EVENTS.UNLOCKED
        self.__coin_position   = 0

        self.__create_grid()

        self.__chip_pl1.set_chip_color(gbChipPl1)
        self.__chip_pl1.set_chip_size(self.__chip_size)
        self.__chip_pl1.set_design(gbChipDesign)

        self.__chip_pl2.set_chip_color(gbChipPl2)
        self.__chip_pl2.set_design(gbChipDesign)
        self.__chip_pl2.set_chip_size(self.__chip_size)

    def __wait_for(self, tmMilSec) -> bool:
        if self.__wait_diff == 0:
            self.__wait_diff = pg.time.get_ticks() + tmMilSec

        elif self.__wait_diff > pg.time.get_ticks():
            return False

        elif self.__wait_diff <= pg.time.get_ticks():
            return True

    def game_result(self) -> int:
        return self.__game_result

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

    def __is_column_full(self, coin_position) -> bool:
        for x in range(0, 6):
            if self.__game_grid[coin_position][5 - x] == 0:
                return False

            else:
                continue

        return True

    def drop_coin(self):
        if not self.__is_column_full(self.__coin_position):
            for x in range(0, 6):
                if self.__game_grid[self.__coin_position][5 - x] == 0:  # Welche Position in der Spalte ist frei?
                    self.__free_coin_place  = 5 - x
                    self.__lock_key_events  = KEY_EVENTS.LOCKED
                    self.__anim_insert_coin = True
                    self.__Audio.play_coin_insert()
                    return

                else:
                    continue

    def __animation_coin_insert(self) -> None:
        if self.__wait_diff <= pg.time.get_ticks():
            self.__wait_diff = pg.time.get_ticks() + self.__game_speed
            self.__column_count += 1

        if self.__column_count == self.__free_coin_place:
            self.__anim_insert_coin = False
            self.__column_count     = -1
            self.__wait_diff        = 0
            self.__after_coin_insert()
            return

        if self.__am_zug == 1:
            self.__chip_pl1.draw_chip_pos(170 + (self.__coin_position * 80), 170 + (self.__column_count * 70))

        elif self.__am_zug == 2:
            self.__chip_pl2.draw_chip_pos(170 + (self.__coin_position * 80), 170 + (self.__column_count * 70))

    def __after_coin_insert(self) -> None:
        self.__game_grid[self.__coin_position][self.__free_coin_place] = self.__am_zug  # Set Coin to GameGrid
        self.__game_result = self.__grid_check()

        if self.__game_result != 0:
            self.__Audio.play_win()

        # Ergebnisausgabe auf Konsole [Testzweck]
        '''
        if self.__game_result == 1:
            print('Spieler 1 gewinnt!')

        elif self.__game_result == 2:
            print('Spieler 2 gewinnt!')

        elif self.__game_result == 3:
            print('Unentschieden!')
        '''

        if self.__am_zug == 1 and self.__game_mode == GAME_MODE.PL_VS_CPU:  # Spielerwechsel Sp1 auf CPU
            self.__am_zug = 2

        elif self.__am_zug == 1 and self.__game_mode == GAME_MODE.PL_VS_PL:  # Spielerwechsel Sp1 auf Sp2
            self.__lock_key_events = KEY_EVENTS.UNLOCKED
            self.__am_zug = 2

        elif self.__am_zug == 2:  # Spielerwechsel CPU/Sp2 auf Sp1
            self.__lock_key_events = KEY_EVENTS.UNLOCKED
            self.__am_zug = 1

    def __draw_board(self) -> None:
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 150], [120, 130, 580, 430], 0, 1, 20, 20, 20, 20)
        pg.draw.rect(self.__BackBufferScreen, [0, 100, 150], [120, 130, 580, 430], 3, 20)

        for x in range(0, 7):
            for y in range(0, 6):
                pg.draw.circle(self.__BackBufferScreen, [0, 0, 20], [170 + (x * 80), 170 + (y * 70)],
                               self.__chip_size + 2, 0)
                pg.draw.circle(self.__BackBufferScreen, [0, 100, 150], [170 + (x * 80), 170 + (y * 70)],
                               self.__chip_size + 2 , 3)

        self.__draw_coin_grid()

    def __draw_coin_grid(self) -> None:
        for x in range(0, 7):
            for y in range(0, 6):
                if self.__game_grid[x][y] == 1:
                    self.__chip_pl1.draw_chip_pos(170 + (x * 80), 170 + (y * 70))
                elif self.__game_grid[x][y] == 2:
                    self.__chip_pl2.draw_chip_pos(170 + (x * 80), 170 + (y * 70))

    def __grid_check_column(self) -> int:  # Sind 4 Chips in einer Reihe?
        for y in range(0, 6):
            for x in range(0, 4):
                if self.__game_grid[x][5 - y] == 1 and self.__game_grid[x + 1][5 - y] == 1\
                        and self.__game_grid[x + 2][5 - y] == 1 and self.__game_grid[x + 3][5 - y] == 1:
                    return 1

                elif self.__game_grid[x][5 - y] == 2 and self.__game_grid[x + 1][5 - y] == 2\
                        and self.__game_grid[x + 2][5 - y] == 2 and self.__game_grid[x + 3][5 - y] == 2:
                    return 2

        return 0

    def __grid_check_row(self) -> int:  # Sind 4 Chips in einer Spalte?
        for x in range(0, 7):
            for y in range(0, 3):
                if self.__game_grid[x][y] == 1 and self.__game_grid[x][y + 1] == 1\
                        and self.__game_grid[x][y + 2] == 1 and self.__game_grid[x][y + 3] == 1:
                    return 1

                elif self.__game_grid[x][y] == 2 and self.__game_grid[x][y + 1] == 2\
                        and self.__game_grid[x][y + 2] == 2 and self.__game_grid[x][y + 3] == 2:
                    return 2

        return 0

    def __grid_check_diagonal(self) -> int:   # Sind 4 Chips in einer diagonale?
        for y in range(0, 3):
            for x in range(0, 4):
                # Direction: to right
                if self.__game_grid[x][y + 3] == 1 and self.__game_grid[x + 1][y + 2] == 1\
                        and self.__game_grid[x + 2][y + 1] == 1 and self.__game_grid[x + 3][y] == 1:
                    return 1

                elif self.__game_grid[x][y + 3] == 2 and self.__game_grid[x + 1][y + 2] == 2\
                        and self.__game_grid[x + 2][y + 1] == 2 and self.__game_grid[x + 3][y] == 2:
                    return 2

                # Direction_ left
                if self.__game_grid[6 - x][y + 3] == 1 and self.__game_grid[5 - x][y + 2] == 1\
                        and self.__game_grid[4 - x][y + 1] == 1 and self.__game_grid[3 - x][y] == 1:
                    return 1

                elif self.__game_grid[6 - x][y + 3] == 2 and self.__game_grid[5 - x][y + 2] == 2\
                        and self.__game_grid[4 - x][y + 1] == 2 and self.__game_grid[3 - x][y] == 2:
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

    def __grid_check(self) -> int:  # Prüfung des Gitters, ob VierGewinnt-Regeln erfüllt wurden
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

        if self.__game_result == 0:
            if self.__anim_insert_coin:
                self.__animation_coin_insert()

            else:
                if self.__am_zug == 1:                                                  # Bewegung durch Spieler 1
                    self.__chip_pl1.draw_chip_pos(170 + (self.__coin_position * 80), 90)

                elif self.__am_zug == 2 and self.__game_mode == GAME_MODE.PL_VS_CPU:    # Bewegung durch CPU
                    self.__cpu_player()

                elif self.__am_zug == 2 and self.__game_mode == GAME_MODE.PL_VS_PL:     # Bewegung durch Spieler 2
                    self.__chip_pl2.draw_chip_pos(170 + (self.__coin_position * 80), 90)

        elif self.__game_result != 0:                                                   # Gewonnen | Unentschieden
            self.__lock_key_events = KEY_EVENTS.LOCKED
            pg.draw.rect(self.__BackBufferScreen, [0, 0, 20], [200, 200, 420, 150], 0)
            pg.draw.rect(self.__BackBufferScreen, [0, 255, 0], [200, 200, 420, 150], 3)

            if self.__game_result == 1:
                self.__gtWin.setTextName('!! Spieler 1 hat gewonnen !!')

            elif self.__game_result == 2 and self.__game_mode == GAME_MODE.PL_VS_CPU:
                self.__gtWin.setTextName('    !! CPU hat gewonnen !!')

            elif self.__game_result == 2 and self.__game_mode == GAME_MODE.PL_VS_PL:
                self.__gtWin.setTextName('!! Spieler 2 hat gewonnen !!')

            elif self.__game_result == 3:
                self.__gtWin.setTextName('      !! Unentschieden !!')

            self.__gtWin.drawText()
            self.__gtWeiter.drawText()

    def __cpu_player(self) -> None:
        self.__chip_pl2.draw_chip_pos(170 + (self.__coin_position * 80), 90)

        if self.__wait_for(200):
            self.__wait_diff = 0

            if self.__cpu_access_ones:
                self.__cpu_access_ones = False
                if self.__cpu_difficulty == DIFFICULTY.STUPID:
                    self.__cpu_stupid_grid_check()

                elif self.__cpu_difficulty == DIFFICULTY.NORMAL:
                    self.__cpu_normal_grid_check()

                elif self.__cpu_difficulty == DIFFICULTY.DIFFICULT:
                    self.__cpu_difficult_grid_check()

            if self.__coin_position > self.__cpu_drop_position:
                self.decrement_coin_position()

            elif self.__coin_position < self.__cpu_drop_position:
                self.increment_coin_position()

            elif self.__coin_position == self.__cpu_drop_position:
                self.__cpu_access_ones = True
                self.drop_coin()

    def __cpu_stupid_grid_check(self) -> None:
        while True:
            self.__cpu_drop_position = randint(0, 6)
            if not self.__is_column_full(self.__cpu_drop_position):
                break

    def __cpu_normal_grid_check(self) -> None:
        if self.__signature_1_1() and self.__signature_1_2()\
                and self.__signature_2()\
                and self.__signature_3()\
                and self.__signature_4():
            print('Random')
            self.__cpu_stupid_grid_check()

    def __signature_1_1(self) -> bool:
        for y in range(0, 6):
            if self.__game_grid[0][5-y] == 1 and self.__game_grid[1][5-y] == 1\
                    and self.__game_grid[2][5-y] == 1:
                if self.__game_grid[3][5-y] == 0 and y == 0:
                    self.__cpu_drop_position = 3
                    print('Sig1.1: C1')
                    return False

                elif self.__game_grid[3][5 - y] == 0 and y != 0:
                    if self.__game_grid[3][5-y+1] != 0:
                        self.__cpu_drop_position = 3
                        print('Sig1.1: C1')
                        return False

            elif self.__game_grid[4][5-y] == 1 and self.__game_grid[5][5-y] == 1\
                    and self.__game_grid[6][5-y] == 1:
                if self.__game_grid[3][5-y] == 0 and y == 0:
                    self.__cpu_drop_position = 3
                    print('Sig1.1: C2')
                    return False

                elif self.__game_grid[3][5-y] == 0 and y != 0:
                    if self.__game_grid[3][5-y+1] != 0:
                        self.__cpu_drop_position = 3
                        print('Sig1.1: C2')
                        return False

        return True

    def __signature_1_2(self) -> bool:
        tmp_choice_1 = [-1, 0]  # [Wert, Position]
        tmp_choice_2 = [-1, 0]

        for x in range(0, 3):
            for y in range(0, 6):
                if self.__game_grid[1+x][5-y] == 1 and self.__game_grid[2+x][5-y] == 1\
                        and self.__game_grid[3+x][5-y] == 1:
                    if self.__game_grid[x][5-y] == 0 and y == 0:  # Choice1
                        tmp_choice_1 = [0, x]

                    elif self.__game_grid[x][5-y] == 0 and y != 0:
                        if self.__game_grid[x][5-y+1] != 0:
                            tmp_choice_1 = [0, x]

                    if self.__game_grid[x+4][5-y] == 0 and y == 0:  # Choice2
                        tmp_choice_2 = [0, x+4]

                    elif self.__game_grid[x+4][5-y] == 0 and y != 0:
                        if self.__game_grid[x+4][5-y+1] != 0:
                            tmp_choice_2 = [0, x+4]

        if tmp_choice_1[0] == 0 and tmp_choice_2[0] == 0:
            x = randint(0, 1)
            if x == 0:
                self.__cpu_drop_position = tmp_choice_1[1]

            elif x == 1:
                self.__cpu_drop_position = tmp_choice_2[1]

            return False

        elif tmp_choice_1[0] == 0 and tmp_choice_2[0] != 0:
            self.__cpu_drop_position = tmp_choice_1[1]
            return False

        elif tmp_choice_1[0] != 0 and tmp_choice_2[0] == 0:
            self.__cpu_drop_position = tmp_choice_2[1]
            return False

        return True

    def __signature_2(self) -> bool:
        for y in range(0, 6):
            for x in range(0, 4):
                if self.__game_grid[x][5-y] == 1 and self.__game_grid[x+1][5-y] == 1\
                        and self.__game_grid[x+3][5-y] == 1:
                    if self.__game_grid[x+2][5-y] == 0 and y == 0:
                        self.__cpu_drop_position = x + 2
                        return False

                    elif self.__game_grid[x+2][5-y] == 0 and y != 0:
                        if self.__game_grid[x+2][5-y+1] != 0:
                            self.__cpu_drop_position = x + 2
                            return False

        return True

    def __signature_3(self) -> bool:
        for y in range(0, 6):
            for x in range(0, 4):
                if self.__game_grid[x][5 - y] == 1 and self.__game_grid[x + 2][5 - y] == 1 \
                        and self.__game_grid[x + 3][5 - y] == 1:
                    if self.__game_grid[x + 1][5 - y] == 0 and y == 0:
                        self.__cpu_drop_position = x + 1
                        return False

                    elif self.__game_grid[x + 1][5 - y] == 0 and y != 0:
                        if self.__game_grid[x + 1][5 - y + 1] != 0:
                            self.__cpu_drop_position = x + 1
                            return False

        return True

    def __signature_4(self) -> bool:
        for y in range(0, 3):
            for x in range(0, 7):
                if self.__game_grid[x][5-y] == 1 and self.__game_grid[x][4-y] == 1\
                        and self.__game_grid[x][3-y] == 1:
                    if self.__game_grid[x][2-y] == 0:
                        self.__cpu_drop_position = x
                        return False

        return True

    def __signature_5(self) -> bool:
        pass

    def __signature_6(self) -> bool:
        pass

    def __signature_7(self) -> bool:
        pass

    def __signature_8(self) -> bool:
        pass

    def __signature_9(self) -> bool:
        pass

    def __signature_10(self) -> bool:
        pass

    def __cpu_difficult_grid_check(self) -> None:
        pass

    def __create_grid(self) -> None:
        self.__game_grid.clear()
        for x in range(0, 7):
            tmp = []
            for y in range(0, 6):
                tmp.append(0)
            self.__game_grid.append(tmp)

    def print_grid_to_console(self) -> None:  # Ausgabe des Spielrasters auf Konsole über "g"-Taste [Testzweck]
        print('----- Game Grid -----')
        for y in range(0, 6):
            for x in range(0, 7):
                print('[' + str(self.__game_grid[x][y]) + ']', end = '')
            print('')

































