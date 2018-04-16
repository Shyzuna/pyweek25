"""
Title: GameManager
Desc: Main classes containing all the basics for game execution
Creation: 15/04/18
Last Mod: 15/04/18
TODO:
    * May split with DisplayManager
    * Is a manger list to propagate is needed
"""

import pygame
import settings.settings as settings

from modules.managers.InputManager import myInputManager
from modules.managers.GuiManager import myGuiManager


class GameManager(object):
    """
        GameManager class
    """
    def __init__(self):
        """
            Init base elements
        """
        self._running = True
        self._init = False
        self._display = None
        self._clock = None
        self._debug = settings.DEBUG
        self._managerList = {
            'Game': self,
            'Input': myInputManager,
            'Gui': myGuiManager
        }

        self.deltaTime = 0

    def init(self):
        """
        Init pygame and display
        :return: Nothing
        """
        pygame.init()
        self._display = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.HWSURFACE)
        self._clock = pygame.time.Clock()
        self._running = True

        for manager in self._managerList.values():
            if manager != self:
                manager.init(self._managerList)

        self._init = True

    def start(self):
        """
        Entry point to start the game
        :return: Nothing
        """
        if not self._init:
            self.init()

        self.mainLoop()
        self.cleanExit()

    def stop(self):
        """
        Stop the main loop at the next loop
        :return: Nothing
        """
        self._running = False

    def cleanExit(self):
        """
        Clean up before exiting
        :return: Nothing
        """
        pygame.quit()

    def render(self):
        """
        Render elements in scene (Clean/Render/Flip)
        :return: Nothing
        """
        self._display.fill((0, 0, 0))
        if self._debug:
            self._managerList['Gui'].writeText(self._clock.get_fps(), 'Arial', (255, 0, 0), (0, 0))
        pygame.display.flip()

    def display(self, elem, pos):
        self._display.blit(elem,pos)

    def mainLoop(self):
        """
        Principal game loop
        :return: Nothing
        """
        while self._running:
            self._clock.tick(settings.FPS)
            self.deltaTime = self._clock.get_time()
            myInputManager.handleEvents()
            self.render()


myGameManager = GameManager()
