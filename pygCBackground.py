
# ####################################################
# Class       : CBackground
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-19
# Version     : V1.0
# ####################################################
# Description
# ===========
# Raster aus schwach blauen Kugel als Hintergrund
#
# ####################################################

# Import
import pygame as pg


# Class
class CBackgrund:
    def __init__(self, toBuffer):
        self.__BackBufferScreen = toBuffer

    def drawBGDarkBlue(self):
        self.__BackBufferScreen.fill((0, 0, 20))

    def drawBGGridballs(self):
        self.__BackBufferScreen.fill((0, 0, 20))

        for y in range(0, 6):
            for x in range(0, 7):
                for i in range(0, 100):
                    pg.draw.circle(self.__BackBufferScreen, [0, 0, 20 + (0.3 * i)],
                                   [100 + (x * 100), 100 + (y * 85)], 40 - (0.4 * i), 0)
