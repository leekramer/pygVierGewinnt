
# #################################################################################################
# Class       : CText
# Dependencies: pygame
# Developer   : Lee Kramer
# Developed   : 2022-06-10
# Version     : V1.1
# #################################################################################################
# Description
# ===========
# Verknüpfung, Verwaltung & Darstellung von
# Text in einer PyGame-Anwendung.
#
# #################################################################################################

# Import
import pygame as pg


# Class
class CText:
    def __init__(self, toBuffer, injAttr=None, tTextName='Text', tPosX=0, tPosY=0) -> None:
        self.__BufferScreen  = toBuffer
        if injAttr is None:
            self.__FontType      = 'Arial'
            self.__FontSize      = 20
            self.__FontBold      = False
            self.__FontItalic    = False

            if tTextName == '':
                tTextName = 'Text'

            self.__TextName      = tTextName
            self.__TextAntialias = True
            self.__TextColor     = [255, 255, 255]
            self.__TextPosition  = [tPosX, tPosY]

        elif injAttr is not None:
            self.__FontType      = injAttr[0]
            self.__FontSize      = injAttr[1]
            self.__FontBold      = injAttr[2]
            self.__FontItalic    = injAttr[3]

            self.__TextName      = tTextName
            self.__TextAntialias = injAttr[4]
            self.__TextColor     = injAttr[5]
            self.__TextPosition  = [tPosX, tPosY]

        self.__Text = None
        self.__Font = None

        self.__updateSettings()

    def setFontType(self, fType: str) -> None:
        self.__FontType = fType
        self.__updateSettings()

    def setFontSize(self, fSize: int) -> None:
        self.__FontSize = fSize
        self.__updateSettings()

    def setFontBold(self, fBold: bool) -> None:
        self.__FontBold = fBold
        self.__updateSettings()

    def setItalic(self, fItalic: bool) -> None:
        self.__FontItalic = fItalic
        self.__updateSettings()

    def setTextName(self, tText: str) -> None:
        if tText == '':
            tText = 'Text'

        self.__TextName = tText
        self.__updateSettings()

    def setTextAntialias(self, tAntialias: bool) -> None:
        self.__TextAntialias = tAntialias
        self.__updateSettings()

    def setTextColor(self, tColor) -> None:
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

    def extractAttributes(self) -> list:
        tmpAttr = [self.__FontType,
                   self.__FontSize,
                   self.__FontBold,
                   self.__FontItalic,
                   self.__TextAntialias,
                   self.__TextColor]

        return tmpAttr

    def injektAttributesFrom(self, _attributes) -> None:
        self.__FontType      = _attributes[0]
        self.__FontSize      = _attributes[1]
        self.__FontBold      = _attributes[2]
        self.__FontItalic    = _attributes[3]
        self.__TextAntialias = _attributes[4]
        self.__TextColor     = _attributes[5]

    def setTextPosition(self, tPosX: int, tPosY: int) -> None:
        self.__TextPosition = [tPosX, tPosY]

    def __updateSettings(self) -> None:
        self.__Font = pg.font.SysFont(self.__FontType, self.__FontSize, self.__FontBold, self.__FontItalic)
        self.__Text = self.__Font.render(self.__TextName, self.__TextAntialias, self.__TextColor)
        # self.__Text.set_alpha(50) <-- Experimentell [Transparenztest]

    def drawText(self) -> None:
        self.__BufferScreen.blit(self.__Text, self.__TextPosition)
