"""
Title: GameLevel
Desc: Handle a level using a map name
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
    * Other place for convert ?
"""
# coding=utf-8
import pygame

import constants.colors as colors

from modules.widgets.objects.PlayerObject import PlayerObject
from modules.widgets.objects.ScrollWindow import ScrollWindow

from modules.managers.MapManager import myMapManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.GuiManager import myGuiManager


class GameLevel(object):
    def __init__(self, name, myGameManager):
        self._map = name
        self._myGameManager = myGameManager
        self._mapObject = myMapManager.getMap(name)
        self._tilesData = {}
        self._tileSize = myMapManager.getTileSize()
        for key, tile in myMapManager.getTiles().items():
            self._tilesData[key] = tile.convert()
        self._background = pygame.Surface(myDisplayManager.getSize())
        self._background.fill(colors.BLACK)
        self._mapObject.setTileSet(self._tilesData, self._tileSize)
        self._mapObject.setWalkingTiles(['0', '2'])

        self._scrollWindow = ScrollWindow(self._mapObject)
        self._mapObject.setScrollWindow(self._scrollWindow)
        self._player = PlayerObject(self._mapObject, self._scrollWindow)

    def render(self, deltaTime):
        myDisplayManager.display(self._background, (0, 0))
        self._mapObject.render(deltaTime)
        self._player.render(deltaTime)
        self._scrollWindow.render(deltaTime)

    def update(self):
        self._player.update(self._myGameManager.deltaTime)

    def refresh(self):
        pass

    def processEvent(self, event):
        self._player.processEvent(event)
