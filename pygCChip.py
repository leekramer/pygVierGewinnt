
# ####################################################
# Class       : CChip
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-20
# Version     : V1.0
# ####################################################
# Description
# ===========
# Klasse zur Darstellung der Chips
#
# ####################################################

# Import
import pygame as pg


# Class
class CChip:
    def __init__(self, toBuffer, cpColor: int, cpDesign: int):
        self.__BackBufferScreen = toBuffer
        if cpColor < 0 or cpColor > 4:
            self.__color = 0

        else:
            self.__color = cpColor

        if cpDesign < 0 or cpDesign > 3:
            self.__design = 0

        else:
            self.__design = cpDesign

        self.__col_rim    = [0, 0, 0]
        self.__col_body   = [0, 0, 0]
        self.__col_design = [0, 0, 0]

    def set_chip_color(self, cpColor):
        if cpColor < 0 or cpColor > 4:
            self.__color = 0

        else:
            self.__color = cpColor

    def get_chip_color(self):
        return self.__color

    def set_design(self, cpDesign):
        if cpDesign < 0 or cpDesign > 3:
            self.__design = 0

        else:
            self.__design = cpDesign

    def get_design(self):
        return self.__design

    def draw_chip_pos(self, posX: int, posY: int):
        if self.__color == 0:
            self.__col_rim    = [205, 205, 0]
            self.__col_body   = [155, 155, 0]
            self.__col_design = [255, 255, 0]

        elif self.__color == 1:
            self.__col_rim    = [205, 0, 0]
            self.__col_body   = [155, 0, 0]
            self.__col_design = [255, 0, 0]

        elif self.__color == 2:
            self.__col_rim    = [0, 205, 0]
            self.__col_body   = [0, 155, 0]
            self.__col_design = [0, 255, 0]

        elif self.__color == 3:
            self.__col_rim    = [0, 0, 205]
            self.__col_body   = [0, 0, 155]
            self.__col_design = [0, 0, 255]

        elif self.__color == 4:
            self.__col_rim    = [100, 100, 100]
            self.__col_body   = [50, 50, 50]
            self.__col_design = [150, 150, 150]

        pg.draw.circle(self.__BackBufferScreen, self.__col_rim, [posX, posY], 20, 0)
        pg.draw.circle(self.__BackBufferScreen, self.__col_body, [posX, posY], 16, 0)

        if self.__design == 0:  # Default
            pass

        if self.__design == 1:  # Square
            pg.draw.rect(self.__BackBufferScreen, self.__col_design, [posX - 6, posY - 6, 12, 12], 0)

        if self.__design == 2:  # Circle
            pg.draw.circle(self.__BackBufferScreen, self.__col_design, [posX, posY], 7, 0)

        if self.__design == 3:  # Scratch
            pg.draw.line(self.__BackBufferScreen, self.__col_design, [posX - 5, posY + 5], [posX + 5, posY - 5])
            pg.draw.line(self.__BackBufferScreen, self.__col_design, [posX - 7, posY + 3], [posX + 3, posY - 7])
            pg.draw.line(self.__BackBufferScreen, self.__col_design, [posX - 3, posY + 7], [posX + 7, posY - 3])

    def draw_chip(self, posX: int, posY: int, cpColor: int, cpDesign: int):
        self.set_chip_color(cpColor)
        self.set_design(cpDesign)
        self.draw_chip_pos(posX, posY)
