
# ####################################################
# Class       : CRulesBackground
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-19
# Version     : V1.0
# ####################################################
# Description
# ===========
# Hintergrund für die Rules Loop-Page
#
# ####################################################

# Import
import pygame as pg


# Class
class CRulesBackgrund:
    def __init__(self, toBuffer, bgPosition, bgSize):
        self.__BackBufferScreen = toBuffer
        self.__Position = bgPosition
        self.__Size     = bgSize
        self.__radius   = 40
        self.__Color    = [0, 0, 255]

    def __drawRectangle(self):
        pg.draw.rect(self.__BackBufferScreen, [0, 0, 10],
                     [self.__Position[0], self.__Position[1], self.__Size[0], self.__Size[1]], 0)

    def __drawCircle(self, posX, posY):
        r_range = self.__radius / 100
        c_range = 30 / 100
        for i in range(0, 100):
            pg.draw.circle(self.__BackBufferScreen, [0, 0, 10 + (c_range * i)],
                           [posX, posY], self.__radius - (r_range * i), 0)

    def drawBackground(self):
        self.__drawRectangle()
        for y in range(0, 6):
            for x in range(0, 7):
                self.__drawCircle(100 + (x * 100), 100 + (y * 85))
