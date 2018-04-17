"""
Title: MapObject
Desc: Used by MapManager to aggregate map's data and to render it
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
    * collision checking here ok ? or create an other manager ?
"""
# coding=utf-8

from modules.managers.DisplayManager import myDisplayManager


class MapObject(object):
    def __init__(self, name):
        self._name = name
        self._size = None
        self._loaded = False
        self._mapData = None

        self._tiles = None
        self._tileSize = None

    def load(self, size, mapData):
        self._mapData = mapData
        self._size = size
        self._loaded = True

    def setTileSet(self, tiles, tileSize):
        self._tiles = tiles
        self._tileSize = tileSize

    def render(self, deltaTime):
        tileW, tileH = self._tileSize
        positionT = 0
        positionL = 0
        for x in range(len(self._mapData)):
            line = self._mapData[x]
            for y in range(len(line)):
                case = line[y]
                if case != ' ':
                    myDisplayManager.display(self._tiles[case], (positionL, positionT))
                positionL += tileW
            positionL = 0
            positionT += tileH

    def pixelToMap(self, x, y):
        return x // self._tileSize[0], y // self._tileSize[1]

    def checkCollision(self, rect):
        cornerList = [
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top),
            (rect.left + rect.width, rect.top + rect.height),
            (rect.left, rect.top + rect.height),
        ]
        collide = False
        for corner in cornerList:
            mapPointX, mapPointY = self.pixelToMap(corner[0], corner[1])
            # Line first then Case
            if self._mapData[mapPointY][mapPointX] != '0':
                return True
        return collide
