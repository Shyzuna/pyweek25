"""
Title: DisplayManager
Desc: Handle display and options
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
"""

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
        self._managerList = None

        self.sizes = None

    def init(self, managerList):
        """
        Init display
        :return: Nothing
        """
        self._managerList = managerList
        self.sizes = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        flags = (pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN) if settings.FULL_SCREEN \
            else (pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display = pygame.display.set_mode(self.sizes, flags)
        pygame.display.set_caption(settings.TITLE)
        self._init = True

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
            return ((self.sizes[0] - subElemSizes[0]) / 2.0), ((self.sizes[1] - subElemSizes[1]) / 2.0)

myDisplayManager = DisplayManager()
