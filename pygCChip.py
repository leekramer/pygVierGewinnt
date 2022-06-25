
# #################################################################################################
# Class       : CChip
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-20
# Version     : V1.0
# #################################################################################################
# Description
# ===========
# Klasse zur Darstellung der Chips
#
# #################################################################################################

# Import
import pygame as pg
import enum


# Enum
class CHIP_COLOR(enum.IntEnum):
    YELLOW   = 0
    RED      = 1
    GREEN    = 2
    BLUE     = 3
    GREY     = 4

class CHIP_DESIGN(enum.IntEnum):
    STANDARD = 0
    SQUARE   = 1
    CIRCLE   = 2
    SCRATCH  = 3


# Class
class CChip:
    def __init__(self, toBuffer, cpColor=0, cpDesign=0, cpSize=20) -> None:
        self.__BackBufferScreen = toBuffer
        self.__chip_size        = cpSize

        self.__col_rim          = [0, 0, 0]
        self.__col_body         = [0, 0, 0]
        self.__col_design       = [0, 0, 0]

        if cpColor < 0 or cpColor > 4:
            self.__color = CHIP_COLOR.YELLOW

        else:
            self.__color = cpColor

        if cpDesign < 0 or cpDesign > 3:
            self.__design = CHIP_DESIGN.STANDARD

        else:
            self.__design = cpDesign

    def set_chip_size(self, cpSize) -> None:
        self.__chip_size = cpSize

    def set_chip_color(self, cpColor: int) -> None:
        if cpColor < 0 or cpColor > 4:
            self.__color = CHIP_COLOR.YELLOW

        else:
            self.__color = cpColor

    def get_chip_color(self) -> int:
        return self.__color

    def set_design(self, cpDesign: int) -> None:
        if cpDesign < 0 or cpDesign > 3:
            self.__design = CHIP_DESIGN.STANDARD

        else:
            self.__design = cpDesign

    def get_design(self) -> int:
        return self.__design

    def draw_chip_pos(self, posX: int, posY: int) -> None:
        if self.__color == CHIP_COLOR.YELLOW:
            self.__col_rim    = [205, 205, 0]
            self.__col_body   = [155, 155, 0]
            self.__col_design = [255, 255, 0]

        elif self.__color == CHIP_COLOR.RED:
            self.__col_rim    = [205, 0, 0]
            self.__col_body   = [155, 0, 0]
            self.__col_design = [255, 0, 0]

        elif self.__color == CHIP_COLOR.GREEN:
            self.__col_rim    = [0, 205, 0]
            self.__col_body   = [0, 155, 0]
            self.__col_design = [0, 255, 0]

        elif self.__color == CHIP_COLOR.BLUE:
            self.__col_rim    = [0, 0, 205]
            self.__col_body   = [0, 0, 155]
            self.__col_design = [0, 0, 255]

        elif self.__color == CHIP_COLOR.GREY:
            self.__col_rim    = [100, 100, 100]
            self.__col_body   = [50, 50, 50]
            self.__col_design = [150, 150, 150]

        pg.draw.circle(self.__BackBufferScreen, self.__col_rim, [posX, posY], self.__chip_size, 0)
        pg.draw.circle(self.__BackBufferScreen, self.__col_body, [posX, posY], self.__chip_size * 0.8, 0)

        if self.__design == 0:  # Default
            pass

        if self.__design == 1:  # Square
            ratio = self.__chip_size * 0.3  # Viereck-Design = 30% von Chipgröße
            pg.draw.rect(self.__BackBufferScreen, self.__col_design,
                         [posX - ratio, posY - ratio, ratio * 2, ratio * 2], 0)

        if self.__design == 2:  # Circle
            ratio = self.__chip_size * 0.3  # Kreis-Design = 30% von Chipgröße
            pg.draw.circle(self.__BackBufferScreen, self.__col_design, [posX, posY], ratio, 0)

        if self.__design == 3:  # Scratch
            ratio  = self.__chip_size * 0.25  # Scratch-Design = 25% von Chipgröße
            offset = self.__chip_size * 0.2   # Linien-Versatz = 20% von Chipgröße
            pg.draw.line(self.__BackBufferScreen, self.__col_design,
                         [posX - ratio, posY + ratio], [posX + ratio, posY - ratio])

            pg.draw.line(self.__BackBufferScreen, self.__col_design,
                         [posX - (ratio + offset), posY + (ratio - offset)],
                         [posX + (ratio - offset), posY - (ratio + offset)])

            pg.draw.line(self.__BackBufferScreen, self.__col_design,
                         [posX - (ratio - offset), posY + (ratio + offset)],
                         [posX + (ratio + offset), posY - (ratio - offset)])

    def draw_chip(self, posX: int, posY: int, cpColor: int, cpDesign: int) -> None:
        self.set_chip_color(cpColor)
        self.set_design(cpDesign)
        self.draw_chip_pos(posX, posY)
