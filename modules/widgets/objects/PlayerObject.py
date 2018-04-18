"""
Title: PlayerObject
Desc: Represent the player in game
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
    * check for passing delta time in update or adding mygamemanager ?
    * fix rotation
    * Add control support like zdsq qwsd and click
"""

# coding=utf-8
import math
import pygame
import os
import settings.settings as settings

import modules.tools.vectorTools as vectorTools

from modules.managers.ResourceManager import myResourceManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.GuiManager import myGuiManager


class PlayerObject(object):
    def __init__(self, mapObject, objId, position=(0, 0), rotation=0):
        self._objId = objId
        self._rotation = rotation
        self._mapObject = mapObject
        self._position = (position[0], position[1])
        self._pixelPos = None
        self._playerSurface = myResourceManager.lookFor('player', 'image',
                                                        os.path.join(settings.OBJECTS_PATH, 'player.png'), True)
        self._width, self._height = self._playerSurface.get_size()
        self._keyDirection = {
            pygame.K_DOWN: False,
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self._speed = 20
        self._orientation = 0
        self._interactableObject = None

    def getPixelPosition(self):
        return self._pixelPos

    def getPixelCenterPosition(self):
        return self._pixelPos[0] + self._width // 2, self._pixelPos[1] + self._height // 2

    def setInteractableObject(self, obj):
        self._interactableObject = obj

    def init(self):
        self._pixelPos = self._mapObject.mapToPixel(self._position[0], self._position[1])

    def render(self, deltaTime):
        surface = self._playerSurface
        """rect = surface.get_rect()
        if self._orientation != 0:
            surface = pygame.transform.rotate(surface, self._orientation)
            newRect = surface.get_rect()
            newRect.center = rect.center
            rect = newRect
        rect.left = self._position[0]
        rect.top = self._position[1]"""
        myDisplayManager.display(surface, self._pixelPos)


    def computeOrientation(self):
        posX, posY = pygame.mouse.get_pos()
        middleX, middleY = self._playerSurface.get_rect().center
        vect1 = (0, -1)  # up vector
        vect2 = (posX - middleX, posY - middleY)  # mouse vector
        self._orientation = vectorTools.angle(vect1, vect2)


    def update(self, deltaTime, scrollWindow):
        newX, newY = self._pixelPos
        currentSpeed = deltaTime * self._speed / 100.0
        directionX = 0
        directionY = 0
        for direction, value in self._keyDirection.items():
            if value:
                if direction in [pygame.K_RIGHT, pygame.K_LEFT]:
                    directionX = currentSpeed * (1 if direction == pygame.K_RIGHT else -1)
                if direction in [pygame.K_UP, pygame.K_DOWN]:
                    directionY = currentSpeed * (1 if direction == pygame.K_DOWN else -1)
        if directionX != 0 or directionY != 0:
            newX += directionX
            newY += directionY
            rect = self._playerSurface.get_rect()
            rect.top = newY
            rect.left = newX
            if not self._mapObject.checkCollision(rect):
                xScroll, yScroll = scrollWindow.checkScrolling(self._pixelPos[0], self._pixelPos[1],
                                                                     (directionX, directionY))
                self._pixelPos = (newX if not xScroll else self._pixelPos[0],
                                  newY if not yScroll else self._pixelPos[1])
        self.computeOrientation()

        if self._interactableObject:
            text = self._interactableObject.getInteractText(self)
            myGuiManager.setTooltip(text)
        else:
            myGuiManager.setTooltip(None)

    def refresh(self):
        pass

    def processEvent(self, event):
        if event.type in [pygame.KEYDOWN, pygame.KEYUP] and event.key in self._keyDirection.keys():
            self._keyDirection[event.key] = (event.type == pygame.KEYDOWN)
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self._interactableObject:
                self._interactableObject.interact(self)

    def checkCollision(self, rect):
        return False
