"""
Title: CasualObject
Desc: Map classic object
Creation: 18/04/18
Last Mod: 18/04/18
TODO:
"""
# coding=utf-8
import os
import pygame
import settings.settings as settings
from modules.managers.ResourceManager import myResourceManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.LangManager import myLangManager
from modules.widgets.objects.PlayerObject import PlayerObject


class CasualObject(object):
    def __init__(self, mapObject, objId, objType, position=(0, 0), rotation=0,
                 isLocked=False, isMoovable=False, isCheckable=False, checkedElement=None):
        self._objId = objId
        self._objType = objType
        self._rotation = rotation
        self._mapObject = mapObject
        self._changed = False
        self._isLocked = isLocked
        self._isMoovable = isMoovable
        self._isCheckable = isCheckable
        self._isInteractable = isMoovable or isCheckable
        self._checkedElement = checkedElement
        self._position = (position[0], position[1])
        self._resources = {
            'chair': myResourceManager.lookFor('chair', 'image',
                                              os.path.join(settings.OBJECTS_PATH, 'chair.png'), True),
            'desk': myResourceManager.lookFor('desk', 'image',
                                                os.path.join(settings.OBJECTS_PATH, 'desk.png'), True),
            'lock': myResourceManager.lookFor('lock', 'image',
                                              os.path.join(settings.OBJECTS_PATH, 'lock.png'), True),
        }

        self._width = None
        self._height = None
        self._pixelPos = None
        self._surface = None
        self._rect = None
        self._tacticalMode = None

    def getPixelPosition(self):
        return self._pixelPos

    def getPixelCenterPosition(self):
        return self._rect.center

    def isInteractable(self):
        return self._isInteractable

    def isMoovable(self):
        return self._isMoovable

    def changeMode(self, mode):
        self._tacticalMode = mode

    def createSurface(self):
        self._pixelPos = self._mapObject.mapToPixel(self._position[0], self._position[1])
        surface = self._resources[self._objType]
        if self._isLocked:
            surface = surface.copy()
            surface.blit(self._resources['lock'], (0, surface.get_size()[1] // 2))

        if self._rotation != 0:
            surface = pygame.transform.rotate(surface, self._rotation)
        self._surface = surface
        rect = surface.get_rect()
        self._rect = pygame.Rect(self._pixelPos[0], self._pixelPos[1], rect.width, rect.height)

    def init(self, mode):
        self._tacticalMode = mode
        self.createSurface()

    def render(self, deltaTime, offsetX, offsetY):
        myDisplayManager.display(self._surface, (self._pixelPos[0] - offsetX, self._pixelPos[1] - offsetY))

    def update(self, deltaTime):
        if self._changed:
            self._changed = False
            self.createSurface()

    def refresh(self):
        pass

    def processEvent(self, event):
        pass

    def checkCollision(self, rect):
        return self._rect.colliderect(rect)

    def getInteractText(self, src):
        text = ''
        if self._isCheckable:
            text += myLangManager.getLabel('interaction.check_object')
        if self._isMoovable:
            if self._isCheckable:
                text += '|'
            text += myLangManager.getLabel('interaction.push_object')
        return text

    def interact(self, src):
        pass
