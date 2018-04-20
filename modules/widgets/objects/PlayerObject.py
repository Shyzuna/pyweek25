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

import constants.colors as colors
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
        self._selected = False
        self._playerSurface = myResourceManager.lookFor('player', 'image',
                                                        os.path.join(settings.OBJECTS_PATH, 'player.png'), True)
        self._width, self._height = self._playerSurface.get_size()
        self._keyDirection = {
            pygame.K_DOWN: False,
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self._speed = 30
        self._orientation = 0
        self._interactableObject = None
        self._linkedObject = None
        self._tacticalMode = None
        self._rect = None
        self._playerData = {
            "hp": 50,
            "mp": 20,
            "step": 5,
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

    def setInteractableObject(self, obj):
        self._interactableObject = obj

    def selectionElementRender(self, deltaTime):
        if self._tacticalMode:
            myDisplayManager.display(self._accessibleCasesSurface, self._accessibleCasesSurfacePosition)

    def createAccessibleCasesSurface(self):
        ## TODO OFFSET & SCROLLING
        tileW, tileH = self._mapObject.getTileSize()
        self._accessibleCases = self._mapObject.accessibleCaseFromIn(self._position, self._playerData['step'])
        self._accessibleCasesSurface = pygame.Surface((self._playerData['step'] * tileW * 3,
                                                       self._playerData['step'] * tileH * 3), pygame.SRCALPHA)
        self._accessibleCasesSurface.fill((0, 0, 0, 0))
        self._accessibleCasesSurfacePosition = self._pixelPos[0] - (self._playerData['step'] * tileW),\
                                               self._pixelPos[1] - (self._playerData['step'] * tileH)
        factorX, factorY = self._position
        factorX -= self._playerData['step']
        factorY -= self._playerData['step']
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
        if self._selected:
            self.selectionElementRender(deltaTime)
        myDisplayManager.display(surface, self._pixelPos)


    def computeOrientation(self):
        posX, posY = pygame.mouse.get_pos()
        middleX, middleY = self._playerSurface.get_rect().center
        vect1 = (0, -1)  # up vector
        vect2 = (posX - middleX, posY - middleY)  # mouse vector
        self._orientation = vectorTools.angle(vect1, vect2)


    def moveRealTime(self, deltaTime, scrollWindow):
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
            if not self._mapObject.checkCollision(rect, self):
                xScroll, yScroll = scrollWindow.checkScrolling(self._pixelPos[0], self._pixelPos[1],
                                                               (directionX, directionY))
                self._pixelPos = (newX if not xScroll else self._pixelPos[0],
                                  newY if not yScroll else self._pixelPos[1])
                self._rect = pygame.Rect(self._pixelPos[0], self._pixelPos[1], self._width, self._height)
                xReal, yReal = self._mapObject.applyOffset(self._pixelPos[0], self._pixelPos[1], True)
                self._position = self._mapObject.pixelToMap(xReal, yReal)

    def update(self, deltaTime, scrollWindow):
        if not self._tacticalMode:
            self.moveRealTime(deltaTime, scrollWindow)
        else:
            pass

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._interactableObject and self._interactableObject.isMoovable():
                self._linkedObject = self._interactableObject
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self._interactableObject:
                self._interactableObject.interact(self)
        if event.type == pygame.MOUSEBUTTONUP:
            if self._selected:
                xMouse, yMouse = pygame.mouse.get_pos()
                xReal, yReal = self._mapObject.applyOffset(xMouse, yMouse, True)
                tile = self._mapObject.pixelToMap(xReal, yReal)
                if tile in self._accessibleCases:
                    ## TODO OFFSET & SCROLLING
                    self._position = tile
                    self._pixelPos = self._mapObject.mapToPixel(self._position[0], self._position[1])
                    self._rect = pygame.Rect(self._pixelPos[0], self._pixelPos[1], self._width, self._height)
                    self.createAccessibleCasesSurface()
                    return True  # deny event

    def checkCollision(self, rect, src):
        rect.left, rect.top = self._mapObject.applyOffset(rect.left, rect.top)
        return self._rect.colliderect(rect)

    def getInfo(self):
        return self._playerData

    def getPosition(self):
        return self._position

    def getSize(self):
        return self._width, self._height
