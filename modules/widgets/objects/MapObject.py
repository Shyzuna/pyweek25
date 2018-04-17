"""
Title: MapObject
Desc: Used by MapManager to aggregate map's data and to render it
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
    * collision checking here ok ? or create an other manager ?
    * improve collision
    *
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
        self._walkingTiles = []
        self._scrollWindow = None

    def load(self, size, mapData):
        self._mapData = mapData
        self._size = size
        self._loaded = True

    def getPixelMapSize(self):
        return self._size[0] * self._tileSize[0], self._size[1] * self._tileSize[1]

    def setTileSet(self, tiles, tileSize):
        self._tiles = tiles
        self._tileSize = tileSize

    def setWalkingTiles(self, walkingTiles):
        self._walkingTiles = walkingTiles

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

    def pixelToMap(self, x, y):
        return int(x // self._tileSize[0]), int(y // self._tileSize[1])

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
        return collide

    def setScrollWindow(self, scrollWindow):
        self._scrollWindow = scrollWindow