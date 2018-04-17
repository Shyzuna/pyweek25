"""
Title: MapManager
Desc: Load tiles and maps managing objects and tiles
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
"""
# coding=utf-8

import os
import pygame
import settings.settings as settings

from modules.widgets.objects.MapObject import MapObject



class MapManager(object):
    def __init__(self):
        self._tiles = {
            'aeration': 2,
            'blank': 0,
            'wall': 1
        }
        self._tilesData = {}
        self._tileSize = None
        self._mapList = ['labo']
        self._mapObjects = {}
        self._managerList = None
        self._init = False

    def init(self, managerList):
        self._managerList = managerList
        for myMap in self._mapList:
            self.loadMap(myMap)
        self.loadTiles()
        self._init = True

    def getTiles(self):
        return self._tilesData

    def getTileSize(self):
        return self._tileSize

    def getMap(self, name):
        if name in self._mapObjects.keys():
            return self._mapObjects[name]
        else:
            print("[MapManager] - Unknown map : " + name)
            return None

    def loadTiles(self):
        for tile in self._tiles.keys():
            try:
                self._tilesData[str(self._tiles[tile])] = pygame.image.load(os.path.join
                                                                            (settings.TILES_PATH, tile + '.png'))
            except Exception as e:
                print("[MapManager] - Error while loading tile : " + tile)
                print(e)
        if len(self._tilesData) > 0:
            self._tileSize = list(self._tilesData.values())[0].get_size()

    def loadMap(self, name):
        currentMap = MapObject(name)
        width = 0
        maxWidth = 0
        height = 0
        mapData = []
        currentLine = []
        try:
            with open(os.path.join(settings.MAPS_PATH, name + '.map'), 'r') as file:
                while True:
                    line = file.readline()
                    if line:
                        height += 1
                        width = 0
                        for c in line:
                            if c != '\n':
                                width += 1
                                currentLine.append(c)
                        mapData.append(currentLine)
                        currentLine = []
                    else:
                        break
                    if width > maxWidth:
                        maxWidth = width
                currentMap.load((maxWidth, height), mapData)
                self._mapObjects[name] = currentMap
        except Exception as e:
            print("[MapManager] - Error while loading map : " + name)
            print(e)


myMapManager = MapManager()