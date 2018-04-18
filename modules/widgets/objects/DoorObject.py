"""
Title: DoorObject
Desc: Map object door 
Creation: 18/04/18
Last Mod: 18/04/18
TODO:
    * Maybe make an image manager if too low perf (loading too long)
"""
# coding=utf-8
import os
import pygame
import settings.settings as settings
from modules.managers.ResourceManager import myResourceManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.LangManager import myLangManager
from modules.widgets.objects.PlayerObject import PlayerObject


class DoorObject(object):
    def __init__(self, mapObject, objId, position=(0, 0), rotation=0, isLocked=False, isOpen=True):
        self._objId = objId
        self._rotation = rotation
        self._mapObject = mapObject
        self._changed = False
        self._isLocked = isLocked
        self._isOpen = isOpen
        self._isInteractable = True
        self._position = (position[0], position[1])
        self._resources = {
            'open': myResourceManager.lookFor('door_open', 'image',
                                              os.path.join(settings.OBJECTS_PATH, 'door_open.png'), True),
            'closed': myResourceManager.lookFor('door_closed', 'image',
                                                os.path.join(settings.OBJECTS_PATH, 'door_closed.png'), True),
            'lock': myResourceManager.lookFor('lock', 'image',
                                              os.path.join(settings.OBJECTS_PATH, 'lock.png'), True),
        }

        self._width = None
        self._height = None
        self._pixelPos = None
        self._surface = None
        self._rect = None

    def getPixelPosition(self):
        return self._pixelPos

    def getPixelCenterPosition(self):
        return self._rect.center

    def isInteractable(self):
        return self._isInteractable

    def createSurface(self):
        self._pixelPos = self._mapObject.mapToPixel(self._position[0], self._position[1])
        surface = self._resources['open'] if self._isOpen else self._resources['closed']
        if self._isLocked:
            surface = surface.copy()
            surface.blit(self._resources['lock'], (0, surface.get_size()[1] // 2))

        if self._rotation != 0:
            surface = pygame.transform.rotate(surface, self._rotation)
        self._surface = surface
        rect = surface.get_rect()
        self._rect = pygame.Rect(self._pixelPos[0], self._pixelPos[1], rect.width, rect.height)

    def init(self):
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
        return False if self._isOpen else self._rect.colliderect(rect)

    def getInteractText(self, src):
        # TODO: check for key
        label = 'interaction.'
        label += 'locked_nokey' if self._isLocked else 'door_close' if self._isOpen else 'door_open'
        return myLangManager.getLabel(label)

    def interact(self, src):
        # TODO: check for key
        if type(src) == PlayerObject:
            if not self._isLocked:
                self._isOpen = not self._isOpen
                self.createSurface()
