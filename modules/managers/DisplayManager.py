"""
Title: DisplayManager
Desc: Handle display and options
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
    * Look for list mode and mode ok
"""

# coding=utf-8

import pygame

import settings.settings as settings
import constants.colors as colors


class DisplayManager(object):
    """
        DisplayManager class
    """
    def __init__(self):
        """
            Init base elements
        """
        self._init = False
        self._display = None
        self._fullScreen = None
        self._managerList = None
        self._flags = None
        self._currentResolution = None
        self._availableResolution = []

    def init(self, managerList):
        """
        Init display
        :return: Nothing
        """
        self._managerList = managerList
        self._fullScreen = settings.FULL_SCREEN
        self._availableResolution = settings.AVAILABLE_RESOLUTION
        self._currentResolution = settings.DEFAULT_RESOLUTION
        self._flags = (pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN) if self._fullScreen \
            else (pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.createDisplay()
        pygame.display.set_caption(settings.TITLE)
        self._init = True

    def createDisplay(self):
        self._flags = (pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN) if self._fullScreen \
            else (pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display = pygame.display.set_mode(self._availableResolution[self._currentResolution], self._flags)

    def nextResolution(self):
        self._currentResolution += 1
        self._currentResolution = 0 if self._currentResolution >  len(self._availableResolution) - 1\
            else self._currentResolution
        self.createDisplay()

    def getSize(self):
        return self._availableResolution[self._currentResolution]

    def isFullscreen(self):
        return self._fullScreen

    def toggleFullScreen(self):
        self._fullScreen = not self._fullScreen
        self.createDisplay()

    def display(self, elem, pos):
        self._display.blit(elem, pos)

    def render(self, renderFunctions):
        """
        Render elements in scene (Clean/Render/Flip)
        :return: Nothing
        """
        self._display.fill(colors.WHITE)
        for renderElem in renderFunctions:
            renderElem(self._managerList['Game'].deltaTime)
        pygame.display.flip()

    def getCenterPosition(self, subElemSizes, parentSizes=None, parentPositions=None):
        if parentSizes and parentPositions:
            # center inside parent
            return ((parentSizes[0] - subElemSizes[0]) / 2.0 + parentPositions[0]),\
                   ((parentSizes - subElemSizes[1]) / 2.0 + parentPositions[1])
        else:
            # center inside screen
            return ((self.getSize()[0] - subElemSizes[0]) / 2.0), ((self.getSize()[1] - subElemSizes[1]) / 2.0)

    def getResolutionNumber(self):
        return self._currentResolution


myDisplayManager = DisplayManager()
