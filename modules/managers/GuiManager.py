"""
Title: GuiManager
Desc: Display the menu and user interfaces elements
Creation: 15/04/18
Last Mod: 15/04/18
TODO:
"""

import pygame


class GuiManager(object):
    def __init__(self):
        self._fontList = {}
        self._managerList = None
        self._init = False

    def init(self, managerList):
        self._managerList = managerList
        self._fontList['Arial'] = pygame.font.SysFont('Arial', 15)
        self._init = True

    def writeText(self, text, font, color, position):
        label = self._fontList[font].render(str(text), 1, color)
        self._managerList['Game'].display(label, position)


myGuiManager = GuiManager()
