"""
Title: SelectorObject
Desc: Selector object for tactical mode
Creation: 19/04/18
Last Mod: 19/04/18
TODO:
"""

# coding=utf-8
import os
import pygame
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.ResourceManager import myResourceManager
from modules.managers.GuiManager import myGuiManager
import settings.settings as settings
import constants.colors as colors


class SelectorObject(object):
    def __init__(self, mapObject):
        self._mapObject = mapObject
        self._tacticalMode = None
        self._selectorSurface = myResourceManager.lookFor('selector', 'image',
                                                          os.path.join(settings.OBJECTS_PATH, 'selector.png'), True)
        self._position = (5, 5)
        self._width, self._height = self._selectorSurface.get_size()
        self._selectedObject = None
        self._onObject = None

    def init(self, mode):
        self._tacticalMode = mode

    def render(self, deltaTime):
        basePosition = self._mapObject.mapToPixel(self._position[0], self._position[1])
        myDisplayManager.display(self._selectorSurface, self._mapObject.applyOffset(basePosition[0], basePosition[1]))

    def update(self, deltaTime):
        xMouse, yMouse = pygame.mouse.get_pos()
        xReal, yReal = self._mapObject.applyOffset(xMouse, yMouse, True)
        self._position = self._mapObject.pixelToMap(xReal, yReal)
        self._onObject = self._mapObject.isOnObject(xReal, yReal)
        self.displayGuiContent()

    def refresh(self):
        pass

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            btn1, btn2, btn3 = pygame.mouse

    def displayGuiContent(self):
        content = str(self._position[0]) + 'x' + str(self._position[1])
        if self._onObject:
            content += "|" + self._onObject._objId
        myGuiManager.setSelectorContent(content)
