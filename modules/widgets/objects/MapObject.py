"""
Title: MapObject
Desc: Used by MapManager to aggregate map's data and to render it
Creation: 17/04/18
Last Mod: 18/04/18
TODO:
    * collision checking here ok ? or create an other manager ?
    * improve collision
    * improve objects management maybe split player / person / objects ?
    * improve distances
"""
# coding=utf-8
import pygame
import modules.tools.vectorTools as vectorTools
from modules.managers.DisplayManager import myDisplayManager
from modules.widgets.objects.ScrollWindow import ScrollWindow
from modules.widgets.objects.PlayerObject import PlayerObject


class MapObject(object):
    def __init__(self, name):
        self._name = name
        self._size = None
        self._loaded = False
        self._mapData = None
        self._objects = {}

        self._tiles = None
        self._tileSize = None
        self._walkingTiles = []
        self._scrollWindow = None
        self._ready = False
        self._player = None
        self._proximityFactor = 1.5


    def load(self, size, mapData, objects):
        self._mapData = mapData
        self._size = size
        self._loaded = True
        self._objects = objects
        for elem in self._objects['objects']:
            if type(elem) == PlayerObject:
                self._player = elem
                break

    def loadCustom(self, tiles, tileSize, walkingTiles):
        """
        Load variable data
        :param tiles:
        :param tileSize:
        :param walkingTiles:
        :return:
        """
        self._tiles = tiles
        self._tileSize = tileSize
        self._walkingTiles = walkingTiles
        self._scrollWindow = ScrollWindow(self)
        for elem in self._objects['objects']:
            elem.init()
        self._ready = True

    def refresh(self):
        self._scrollWindow.refresh()

    def render(self, deltaTime):
        offsetX, offsetY = self._scrollWindow.getOffset()
        tileW, tileH = self._tileSize
        positionT = -offsetY
        positionL = -offsetX
        for x in range(len(self._mapData)):
            line = self._mapData[x]
            for y in range(len(line)):
                case = line[y]
                if case != ' ':
                    myDisplayManager.display(self._tiles[case], (positionL, positionT))
                positionL += tileW
            positionL = -offsetX
            positionT += tileH

        for elem in self._objects['objects']:
            if type(elem) == PlayerObject:
                elem.render(deltaTime)
            else:
                elem.render(deltaTime, offsetX, offsetY)

        self._scrollWindow.render(deltaTime)

    def processEvent(self, event):
        for elem in self._objects['objects']:
            elem.processEvent(event)

    def update(self, deltaTime):
        for elem in self._objects['objects']:
            if type(elem) == PlayerObject:
                elem.update(deltaTime, self._scrollWindow)
            else:
                elem.update(deltaTime)

        # call al time ?
        self._player.setInteractableObject(self.closestInteractableElemTo(self._player, self._tileSize[0] * self._proximityFactor))


    def closestInteractableElemTo(self, src, maxDst=None):
        # Modify for center to center ?
        closest = None
        bestValue = None
        srcPos = src.getPixelCenterPosition()
        if src == self._player:
            offsetX, offsetY = self._scrollWindow.getOffset()
            srcPos = (srcPos[0] + offsetX, srcPos[1] + offsetY)
        for elem in self._objects['objects']:
            if elem != src and elem.isInteractable():
                elemPos = elem.getPixelCenterPosition()
                dst = vectorTools.dist(srcPos, elemPos)
                if maxDst and dst <= maxDst:
                    if (bestValue and dst < bestValue) or not bestValue:
                        bestValue = dst
                        closest = elem
        return closest

    def pixelToMap(self, x, y):
        return int(x // self._tileSize[0]), int(y // self._tileSize[1])

    def mapToPixel(self, x, y):
        return int(x * self._tileSize[0]), int(y * self._tileSize[1])

    def getPixelMapSize(self):
        return self._size[0] * self._tileSize[0], self._size[1] * self._tileSize[1]

    def checkCollision(self, rect):
        offsetX, offsetY = self._scrollWindow.getOffset()
        cornerList = [
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top),
            (rect.left + rect.width, rect.top + rect.height),
            (rect.left, rect.top + rect.height),
        ]
        collide = False
        for corner in cornerList:
            mapPointX, mapPointY = self.pixelToMap(corner[0] + offsetX, corner[1] + offsetY)
            if mapPointX < 0 or mapPointX > (self._size[0] - 1)\
                    or mapPointY < 0 or mapPointY > (self._size[1] - 1):  # out of map
                return True
            # Line first then Case
            if self._mapData[mapPointY][mapPointX] not in self._walkingTiles:
                return True

        offsetRect = pygame.Rect(rect.left + offsetX, rect.top + offsetY, rect.width, rect.height)

        for elem in self._objects['objects']:
            if elem.checkCollision(offsetRect):
                return True

        return collide

