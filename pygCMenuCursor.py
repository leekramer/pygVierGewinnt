
# #################################################################################################
# Class       : CMenuCursor
# Dependencies: pygame, pygCText
# Developer   : Lee Kramer
# Developed   : 2022-06-18
# Version     : V1.0
# #################################################################################################
# Description
# ===========
# Blinkender Auswahl-Cursor für die Menü-Navigation
#
# #################################################################################################

# Import
import pygame as pg
import pygCText as pgText


# Class
class CMenuCursor:
    def __init__(self, toBuffer, mcPosition, mcSteps, mcOffset):
        self.__CursorText = pgText.CText(toBuffer, '>', mcPosition[0], mcPosition[1])  # 330, 330
        self.__CursorText.setFontSize(25)
        self.__CursorText.setFontBold(True)
        self.__CursorText.setTextColor([255, 0, 0])

        self.__CursorTime   = 0
        self.__CursorFreq   = 500
        self.__CursorSwap   = False
        self.__CursorPosX   = mcPosition[0]
        self.__CursorPosY   = mcPosition[1]
        self.__CursorState  = 0
        self.__CursorSteps  = mcSteps - 1
        self.__CursorOffset = mcOffset

    def set_next_position(self):
        if self.__CursorState < self.__CursorSteps:
            self.__CursorState += 1
            self.__CursorPosY += self.__CursorOffset
            self.__CursorText.setTextPosition(self.__CursorPosX, self.__CursorPosY)

    def set_prev_position(self):
        if self.__CursorState > 0:
            self.__CursorState -= 1
            self.__CursorPosY -= self.__CursorOffset
            self.__CursorText.setTextPosition(self.__CursorPosX, self.__CursorPosY)

    def is_greater_min(self):
        if self.__CursorState > 0:
            return True

        else:
            return False

    def is_lower_max(self):
        if self.__CursorState < self.__CursorSteps:
            return True

        else:
            return False

    def get_cursor_state(self):
        return self.__CursorState

    def showCursor(self):
        self.__CursorText.drawText()
        if self.__CursorTime == 0:
            self.__CursorTime = pg.time.get_ticks() + self.__CursorFreq

        elif self.__CursorTime < pg.time.get_ticks():
            self.__CursorTime = pg.time.get_ticks() + self.__CursorFreq
            if self.__CursorSwap:
                self.__CursorText.setTextColor([0, 0, 100])
                self.__CursorSwap = False

            elif not self.__CursorSwap:
                self.__CursorText.setTextColor([255, 0, 0])
                self.__CursorSwap = True
