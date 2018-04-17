"""
Title: ScrollWindow
Desc: Define scrolling space for the player/map
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
"""
# coding=utf-8
import pygame
import constants.colors as colors
from modules.managers.DisplayManager import myDisplayManager


class ScrollWindow(object):
    def __init__(self, mapObject):
        self._mapObject = mapObject
        self._offsetX = 0
        self._offsetY = 0
        mapSize = mapObject.getPixelMapSize()
        print(mapSize)
        self._debug = True
        screenW, screenH = myDisplayManager.getSize()
        self._maxOffsetX, self._maxOffsetY = mapSize[0] - screenW, mapSize[1] - screenH
        self._width = 0.5 * screenW
        self._height = 0.5 * screenH
        self._position = myDisplayManager.getCenterPosition((self._width, self._height))
        self._background = pygame.Surface((screenW, screenH), pygame.SRCALPHA)

    def render(self, deltaTime):
        if self._debug:
            self._background.fill((0, 0, 0, 0))
            points = [
                self._position,
                (self._position[0] + self._width, self._position[1]),
                (self._position[0] + self._width, self._position[1] + self._height),
                (self._position[0], self._position[1] + self._height)
            ]
            pygame.draw.lines(self._background, colors.RED, True, points, 2)
            myDisplayManager.display(self._background, (0, 0))

    def checkScrolling(self, oldX, oldY, directions):
        xScroll = False
        yScroll = False

        newX = oldX + directions[0]
        newY = oldY + directions[1]

        if self._position[0] <= oldX <= (self._position[0] + self._width):  # old in X box
            if not self._position[0] <= newX <= (self._position[0] + self._width):  # new out X box
                self._offsetX += directions[0]
                if self._offsetX < 0 or self._offsetX > self._maxOffsetX:
                    self._offsetX = 0 if self._offsetX < 0 else self._maxOffsetX
                else:
                    xScroll = True

        if self._position[1] <= oldY <= (self._position[1] + self._height): # old in y box
            if not self._position[1] <= newY <= (self._position[1] + self._height):  # not in Y box
                self._offsetY += directions[1]
                if self._offsetY < 0 or self._offsetY > self._maxOffsetY:
                    self._offsetY = 0 if self._offsetY < 0 else self._maxOffsetY
                else:
                    yScroll = True

        return xScroll, yScroll

    def getOffset(self):
        return self._offsetX, self._offsetY

    def update(self):
        pass

    def refresh(self):
        pass

    def processEvent(self, event):
        pass