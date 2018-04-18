"""
Title: GuiManager
Desc: Display the menu and user interfaces elements
Creation: 15/04/18
Last Mod: 15/04/18
TODO:
"""

# coding=utf-8

import constants.colors as colors
import pygame


class GuiManager(object):
    def __init__(self):
        self._fontList = {}
        self._managerList = None
        self._init = False
        self._toolTipText = None
        self._toolTipPosition = None

    def init(self, managerList):
        self._managerList = managerList
        screenW, screenH = self._managerList['Display'].getSize()
        self._toolTipPosition = (0.05 * screenW, 0.9 * screenH)
        self._init = True

    def loadFont(self, name, size, sysFont=True):
        fontFullName = name + '-' + str(size)
        if fontFullName not in self._fontList.keys():
            if sysFont:
                self._fontList[fontFullName] = pygame.font.SysFont(name, size)
        return fontFullName

    def createText(self, text, font, size, color, antiAliased=True):
        fontFullName = self.loadFont(font, size)
        return self._fontList[fontFullName].render(str(text), antiAliased, color)

    def writeText(self, text, font, size, color, position):
        label = self.createText(text, font, size, color)
        self._managerList['Display'].display(label, position)

    def estimateSize(self, text, font, size):
        fontFullName = self.loadFont(font, size)
        return self._fontList[fontFullName].size(text)

    def setTooltip(self, text):
        if text:
            self._toolTipText = self.createText(text, 'Lucida Console', 20, colors.RED, False)
        else:
            self._toolTipText = None

    def refresh(self):
        screenW, screenH = self._managerList['Display'].getSize()
        self._toolTipPosition = (0.05 * screenW, 0.9 * screenH)

    def render(self, deltaTime):
        if self._toolTipText:
            self._managerList['Display'].display(self._toolTipText, self._toolTipPosition)


myGuiManager = GuiManager()

