"""
Title: PlayerObject
Desc: Represent the player in game
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
    * check for passing delta time in update or adding mygamemanager ?
    * fix rotation
"""

# coding=utf-8
import math
import pygame
import os
import settings.settings as settings

import modules.tools.vectorTools as vectorTools

from modules.managers.MapManager import myMapManager
from modules.managers.DisplayManager import myDisplayManager


class PlayerObject(object):
    def __init__(self, mapObject, scrollWindow):
        self._playerSurface = pygame.image.load(os.path.join(settings.OBJECTS_PATH, 'player.png')).convert_alpha()
        self._mapObject = mapObject
        self._position = (100, 100)
        self._keyDirection = {
            pygame.K_DOWN: False,
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self._speed = 20
        self._orientation = 0
        self._scrollWindow = scrollWindow

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
        myDisplayManager.display(surface, self._position)

    def computeOrientation(self):
        posX, posY = pygame.mouse.get_pos()
        middleX, middleY = self._playerSurface.get_rect().center
        vect1 = (0, -1)  # up vector
        vect2 = (posX - middleX, posY - middleY)  # mouse vector
        self._orientation = vectorTools.angle(vect1, vect2) #* (-1 if posX > middleX else 1)


    def update(self, deltaTime):
        newX, newY = self._position
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
                xScroll, yScroll = self._scrollWindow.checkScrolling(self._position[0], self._position[1],
                                                                     (directionX, directionY))
                self._position = (newX if not xScroll else self._position[0],
                                  newY if not yScroll else self._position[1])

        self.computeOrientation()

    def refresh(self):
        pass

    def processEvent(self, event):
        if event.type in [pygame.KEYDOWN, pygame.KEYUP] and event.key in self._keyDirection.keys():
            self._keyDirection[event.key] = (event.type == pygame.KEYDOWN)
