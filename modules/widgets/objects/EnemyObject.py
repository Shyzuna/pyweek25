"""
Title: EnemyObject
Desc: Enemy objects for the maps
Creation: 20/04/18
Last Mod: 20/04/18
TODO:
"""
# coding=utf-8

import os
import pygame
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.ResourceManager import myResourceManager
import settings.settings as settings
import constants.colors as colors


class EnemyObject(object):
    def __init__(self, mapObject, objId, position=(0, 0), rotation=0):
        self._objId = objId
        self._rotation = rotation
        self._mapObject = mapObject
        self._position = (position[0], position[1])
        self._pixelPos = None
        self._selected = False
        self._enemySurface = myResourceManager.lookFor('enemy', 'image',
                                                        os.path.join(settings.OBJECTS_PATH, 'opponent.png'), True)
        self._width, self._height = self._enemySurface.get_size()
        self._speed = 30
        self._orientation = 0
        self._tacticalMode = None
        self._rect = None
        self._enemyData = {
            "hp": 30,
            "mp": 10,
            "step": 3,
            "action": 1,
            "consumable": [],
            "spells": [],
            "weapons": []
        }
        self._accessibleCases = None
        self._accessibleCasesSurface = None
        self._accessibleCasesSurfacePosition = None

    def setSelected(self, selected):
        self._selected = selected

    def getPixelPosition(self):
        return self._pixelPos

    def getPixelCenterPosition(self):
        return self._pixelPos[0] + self._width // 2, self._pixelPos[1] + self._height // 2

    def selectionElementRender(self, deltaTime):
        if self._tacticalMode:
            myDisplayManager.display(self._accessibleCasesSurface, self._accessibleCasesSurfacePosition)

    def createAccessibleCasesSurface(self):
        ## TODO OFFSET & SCROLLING
        tileW, tileH = self._mapObject.getTileSize()
        self._accessibleCases = self._mapObject.accessibleCaseFromIn(self._position, self._enemyData['step'])
        self._accessibleCasesSurface = pygame.Surface((self._enemyData['step'] * tileW * 3,
                                                       self._enemyData['step'] * tileH * 3), pygame.SRCALPHA)
        self._accessibleCasesSurface.fill((0, 0, 0, 0))
        self._accessibleCasesSurfacePosition = self._pixelPos[0] - (self._enemyData['step'] * tileW), \
                                               self._pixelPos[1] - (self._enemyData['step'] * tileH)
        factorX, factorY = self._position
        factorX -= self._enemyData['step']
        factorY -= self._enemyData['step']
        print(self._accessibleCasesSurface)
        print(self._position)
        i = 0
        for c in self._accessibleCases:
            print(c)
            x, y = c
            i += 1
            print(i)
            rect = pygame.Rect((x - factorX) * tileW, (y - factorY) * tileH, tileW, tileH)
            print(rect)
            self._accessibleCasesSurface.fill(colors.LIGHT_GREY, rect)

    def changeMode(self, mode):
        self._tacticalMode = mode
        xPos, yPos = self._pixelPos
        xReal, yReal = self._mapObject.applyOffset(xPos, yPos, True)
        self._position = self._mapObject.pixelToMap(xReal, yReal)
        newX, newY = self._mapObject.mapToPixel(self._position[0], self._position[1])
        self._pixelPos = self._mapObject.applyOffset(newX, newY)
        if mode:
            self.createAccessibleCasesSurface()

    def init(self, mode):
        self._pixelPos = self._mapObject.mapToPixel(self._position[0], self._position[1])
        self._rect = pygame.Rect(self._pixelPos[0], self._pixelPos[1], self._width, self._height)
        self._tacticalMode = mode

    def render(self, deltaTime, offsetX, offsetY):
        surface = self._enemySurface
        """rect = surface.get_rect()
        if self._orientation != 0:
            surface = pygame.transform.rotate(surface, self._orientation)
            newRect = surface.get_rect()
            newRect.center = rect.center
            rect = newRect
        rect.left = self._position[0]
        rect.top = self._position[1]"""
        if self._selected:
            self.selectionElementRender(deltaTime)
        myDisplayManager.display(surface, (self._pixelPos[0] - offsetX, self._pixelPos[1] - offsetY))

    def update(self, deltaTime):
        pass


    def refresh(self):
        pass


    def processEvent(self, event):
        pass

    def checkCollision(self, rect, src):
        return self._rect.colliderect(rect)

    def getInfo(self):
        return self._enemyData

    def getPosition(self):
        return self._position

    def getSize(self):
        return self._width, self._height

    def isInteractable(self):
        return False