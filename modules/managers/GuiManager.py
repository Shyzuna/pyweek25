"""
Title: GuiManager
Desc: Display the menu and user interfaces elements
Creation: 15/04/18
Last Mod: 15/04/18
TODO:
"""

# coding=utf-8

import pygame


class GuiManager(object):
    def __init__(self):
        self._fontList = {}
        self._managerList = None
        self._init = False

    def init(self, managerList):
        self._managerList = managerList
        self._init = True

    def loadFont(self, name, size, sysFont=True):
        fontFullName = name + '-' + str(size)
        if fontFullName not in self._fontList.keys():
            if sysFont:
                self._fontList[fontFullName] = pygame.font.SysFont(name, size)
        return fontFullName

    def createText(self, text, font, size, color):
        fontFullName = self.loadFont(font, size)
        return self._fontList[fontFullName].render(str(text), 1, color)

    def writeText(self, text, font, size, color, position):
        label = self.createText(text, font, size, color)
        self._managerList['Display'].display(label, position)

    def estimateSize(self, text, font, size):
        fontFullName = self.loadFont(font, size)
        return self._fontList[fontFullName].size(text)

myGuiManager = GuiManager()
