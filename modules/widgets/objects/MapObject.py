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
import constants.colors as colors
from modules.managers.DisplayManager import myDisplayManager
from modules.widgets.objects.ScrollWindow import ScrollWindow
from modules.widgets.objects.PlayerObject import PlayerObject
from modules.widgets.objects.SelectorObject import SelectorObject


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
        self._proximityFactor = 1.6
        self._tacticalMode = False
        self._tacticalGrid = None
        self._selectorObject = None

    def refresh(self):
        self._selectorObject.refresh()
        self._scrollWindow.refresh()
        self.createGrid()

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

        self._player.render(deltaTime)
        for elem in self._objects['characters']:
            if type(elem) != PlayerObject:
                elem.render(deltaTime, offsetX, offsetY)

        if self._tacticalMode:
            self.displayGrid()

        for elem in self._objects['objects']:
            elem.render(deltaTime, offsetX, offsetY)

        self._selectorObject.render(deltaTime)
        self._scrollWindow.render(deltaTime)


    def getAdjacentCase(self, case):
        caseX, caseY = case
        listCase = []
        if caseX - 1 >= 0:
            listCase.append((caseX - 1, caseY))
        if caseY - 1 >= 0:
            listCase.append((caseX, caseY - 1))
        if caseX + 1 <= self._size[0]:
            listCase.append((caseX + 1, caseY))
        if caseX + 1 <= self._size[1]:
            listCase.append((caseX, caseY + 1))
        return listCase

    def accessibleCaseFromIn(self, case, distance):
        caseList = [case]
        if distance > 0:
            for c in self.getAdjacentCase(case):
                x, y = c
                xReal, yReal = self.mapToPixel(x, y)
                if self._mapData[y][x] in self._walkingTiles and self.isOnObject(xReal, yReal, None) is None:
                    caseList += self.accessibleCaseFromIn(c, distance - 1)

        return list(set(caseList))

    def processEvent(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
            self.toggleMode()

        for elem in self._objects['objects'] + self._objects['characters']:
            if elem.processEvent(event):
                return

        self._selectorObject.processEvent(event)

    def update(self, deltaTime):
        for elem in self._objects['objects'] + self._objects['characters']:
            if type(elem) == PlayerObject:
                elem.update(deltaTime, self._scrollWindow)
            else:
                elem.update(deltaTime)

        self._selectorObject.update(deltaTime)
        # call al time ?
        self._player.setInteractableObject(self.closestInteractableElemTo(self._player, self._tileSize[0] * self._proximityFactor, self._tileSize[0]))

    def load(self, size, mapData, objects):
        self._mapData = mapData
        self._size = size
        self._loaded = True
        self._objects = objects
        for elem in self._objects['characters']:
            if type(elem) == PlayerObject:
                self._player = elem
                break

    def createGrid(self):
        xLine = pygame.Surface((1, self._size[1] * self._tileSize[1]))
        xLine.fill(colors.GRAY)
        yLine = pygame.Surface((self._size[0] * self._tileSize[0], 1))
        yLine.fill(colors.GRAY)
        self._tacticalGrid = [xLine, yLine]

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
        self._selectorObject = SelectorObject(self)
        for elem in self._objects['objects'] + self._objects['characters']:
            elem.init(self._tacticalMode)

        self.createGrid()

        self._ready = True

    def toggleMode(self):
        self._tacticalMode = not self._tacticalMode
        for elem in self._objects['objects'] + self._objects['characters']:
            elem.changeMode(self._tacticalMode)

    def displayGrid(self):
        offsetX, offsetY = self._scrollWindow.getOffset()
        for x in range(self._size[0]):
            myDisplayManager.display(self._tacticalGrid[0], (x * self._tileSize[0] - offsetX, - offsetY))

        for y in range(self._size[1]):
            myDisplayManager.display(self._tacticalGrid[1], (- offsetX, y * self._tileSize[1] - offsetY))

    def closestInteractableElemTo(self, src, maxDst=None, minDst=None):
        # Modify for center to center ?
        closest = None
        bestValue = None
        srcPos = src.getPixelCenterPosition()
        if src == self._player:
            offsetX, offsetY = self._scrollWindow.getOffset()
            srcPos = (srcPos[0] + offsetX, srcPos[1] + offsetY)
        for elem in self._objects['objects'] + self._objects['characters']:
            if elem != src and elem.isInteractable():
                elemPos = elem.getPixelCenterPosition()
                dst = vectorTools.dist(srcPos, elemPos)
                if maxDst and dst <= maxDst:
                    if minDst and dst >= minDst:
                        if (bestValue and dst < bestValue) or not bestValue:
                            bestValue = dst
                            closest = elem
        return closest

    def isOnObject(self, x, y, src):
        rect = pygame.Rect(x, y, self._tileSize[0], self._tileSize[1])
        for elem in self._objects['objects'] + self._objects['characters']:
            if elem.checkCollision(rect, src):
                return elem
        return None

    def applyOffset(self, x, y, add=False):
        offsetX, offsetY = self._scrollWindow.getOffset()
        return x + (1 if add else -1) * offsetX, y + (1 if add else -1) * offsetY

    def pixelToMap(self, x, y):
        return int(x // self._tileSize[0]), int(y // self._tileSize[1])

    def mapToPixel(self, x, y):
        return int(x * self._tileSize[0]), int(y * self._tileSize[1])

    def getPixelMapSize(self):
        return self._size[0] * self._tileSize[0], self._size[1] * self._tileSize[1]

    def getTileSize(self):
        return self._tileSize

    def checkCollision(self, rect, src):
        # TODO care using offset here should be use on one side only
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

        for elem in self._objects['objects'] + self._objects['characters']:
            if elem != src:
                if elem.checkCollision(offsetRect, src):
                    return True

        return collide

