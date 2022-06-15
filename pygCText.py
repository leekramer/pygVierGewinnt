
# ####################################################
# Class       : CText
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-10
# Version     : V1.1
# ####################################################
# Description
# ===========
# Verknüpfung, Verwaltung & Darstellung von
# Text in einer PyGame-Anwendung.
#
# ####################################################

# Import
import pygame as pg


# Class
class CText:
    def __init__(self, toBuffer, tTextName = 'Text', tPosX = 0, tPosY = 0):
        self.__BufferScreen  = toBuffer
        self.__FontType      = 'Arial'
        self.__FontSize      = 20
        self.__FontBold      = False
        self.__FontItalic    = False
        self.__Font          = None

        self.__TextName      = tTextName
        self.__TextAntialias = True
        self.__TextColor     = [255, 255, 255]
        self.__TextPosition  = [tPosX, tPosY]
        self.__Text          = None

        self.__updateSettings()

    def setFontType(self, fType: str):
        self.__FontType = fType
        self.__updateSettings()

    def setFontSize(self, fSize: int):
        self.__FontSize = fSize
        self.__updateSettings()

    def setFontBold(self, fBold: bool):
        self.__FontBold = fBold
        self.__updateSettings()

    def setItalic(self, fItalic: bool):
        self.__FontItalic = fItalic
        self.__updateSettings()

    def setTextName(self, tText: str):
        if tText == '':
            tText = 'Text'

        self.__TextName = tText
        self.__updateSettings()

    def setTextAntialias(self, tAntialias: bool):
        self.__TextAntialias = tAntialias
        self.__updateSettings()

    def setTextColor(self, tColor):
        tColorR, tColorG, tColorB = tColor
        if tColorR < 0 or tColorR > 255:
            tColorR = 255

        if tColorG < 0 or tColorG > 255:
            tColorG = 255

        if tColorB < 0 or tColorB > 255:
            tColorB = 255

        tColor = [tColorR, tColorG, tColorB]

        self.__TextColor = tColor
        self.__updateSettings()

    def setTextPosition(self, tPosX: int, tPosY: int):
        self.__TextPosition = [tPosX, tPosY]

    def __updateSettings(self):
        self.__Font = pg.font.SysFont(self.__FontType, self.__FontSize, self.__FontBold, self.__FontItalic)
        self.__Text = self.__Font.render(self.__TextName, self.__TextAntialias, self.__TextColor)
        # self.__Text.set_alpha(50) <-- Experimentell [Transparenztest]

    def drawText(self):
        self.__BufferScreen.blit(self.__Text, self.__TextPosition)