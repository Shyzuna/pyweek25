"""
Title: SelectorObject
Desc: Selector object for tactical mode
Creation: 19/04/18
Last Mod: 19/04/18
TODO:
    * be carefull with realPos & TilePos & offset
    * small glitch on wider surface for selected cursor
"""

# coding=utf-8
import os
import pygame
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.ResourceManager import myResourceManager
from modules.managers.GuiManager import myGuiManager
from modules.widgets.objects.PlayerObject import PlayerObject
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

        self._selectedSpeed = 5.0
        self._selectedBorderSize = None
        self._selectedCurrentSize = None
        self._selectedSurface = None

    def init(self, mode):
        self._tacticalMode = mode

    def render(self, deltaTime):
        basePosition = self._mapObject.mapToPixel(self._position[0], self._position[1])
        myDisplayManager.display(self._selectorSurface, self._mapObject.applyOffset(basePosition[0], basePosition[1]))
        if self._selectedObject:
            objX, objY = self._selectedObject.getPixelPosition()
            if type(self._selectedObject) != PlayerObject:
                objX, objY = self._mapObject.applyOffset(objX, objY)
            myDisplayManager.display(self._selectedSurface, (objX, objY))

    def updateSelectedCursor(self, deltaTime):
        # could be simplify
        self._selectedCurrentSize += self._selectedSpeed * deltaTime / 100.0
        start = 0 if self._selectedCurrentSize > self._selectedBorderSize else self._selectedCurrentSize
        self._selectedCurrentSize = start
        size = self._selectedBorderSize // 4
        end = start + size
        objW, objH = self._selectedObject.getSize()
        self._selectedSurface = pygame.Surface((objW, objH), pygame.SRCALPHA)
        self._selectedSurface.fill((0, 0, 0, 0))
        selectedSide = 0
        if start > objW:
            selectedSide = 1
            if start > (objW + objH):
                selectedSide = 2
                if start > (2 * objW + objH):
                    selectedSide = 3

        if selectedSide == 0:
            pygame.draw.line(self._selectedSurface, colors.RED, (start, 0), (objW, 0), 4)  # glitch here =D
            if end > objW:
                delta = end - objW
                pygame.draw.line(self._selectedSurface, colors.RED, (objW, 0), (objW, delta), 7)
        elif selectedSide == 1:
            pygame.draw.line(self._selectedSurface, colors.RED, (objW, start - objW), (objW, objH), 7)
            if end > (objW + objH):
                delta = end - (objW + objH)
                pygame.draw.line(self._selectedSurface, colors.RED, (objW, objH), (objW - delta, objH), 7)
        elif selectedSide == 2:
            pygame.draw.line(self._selectedSurface, colors.RED, (objW - (start - (objW + objH)), objH), (0, objH), 7)
            if end > (2 * objW + objH):
                delta = end - (2 * objW + objH)
                pygame.draw.line(self._selectedSurface, colors.RED, (0, objH), (0, objH - delta), 4)
        else:
            pygame.draw.line(self._selectedSurface, colors.RED, (0, objH - (start - (2 * objW + objH))), (0, 0), 4)
            if end > (2 * objW + 2 * objH):
                delta = end - (2 * objW + 2 * objH)
                pygame.draw.line(self._selectedSurface, colors.RED, (0, 0), (delta, 0), 4)

    def update(self, deltaTime):
        xMouse, yMouse = pygame.mouse.get_pos()
        xReal, yReal = self._mapObject.applyOffset(xMouse, yMouse, True)
        self._position = self._mapObject.pixelToMap(xReal, yReal)
        basePosition = self._mapObject.mapToPixel(self._position[0], self._position[1])
        self._onObject = self._mapObject.isOnObject(basePosition[0], basePosition[1], self)
        if self._selectedObject:
            self.updateSelectedCursor(deltaTime)
        self.displayGuiContent()

    def refresh(self):
        pass

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self._selectedObject:
                self._selectedObject.setSelected(False)

            self._selectedObject = self._onObject

            if self._selectedObject:
                self._selectedObject.setSelected(True)
                objW, objH = self._selectedObject.getSize()
                self._selectedBorderSize = 2*objW + 2*objH
                self._selectedCurrentSize = 0
                self.updateSelectedCursor(0)


    def displayGuiContent(self):
        content = str(self._position[0]) + 'x' + str(self._position[1])
        if self._onObject:
            if type(self._onObject) in [PlayerObject]:
                myGuiManager.setPersonSelectorContent(content, self._onObject.getInfo())
            else:
                content += "|" + self._onObject.getInfo()
                myGuiManager.setSelectorContent(content)
        else:
            myGuiManager.setSelectorContent(content)

        if self._selectedObject:
            objX, objY = self._selectedObject.getPosition()
            content = str(objX) + 'x' + str(objY)
            if type(self._selectedObject) in [PlayerObject]:
                myGuiManager.setPersonSelectedContent(content, self._selectedObject.getInfo())
            else:
                content += "|" + self._selectedObject.getInfo()
                myGuiManager.setSelectedContent(content)
        else:
            myGuiManager.setSelectedContent(None)
