"""
Title: GameManager
Desc: Main classes containing all the basics for game execution
Creation: 15/04/18
Last Mod: 16/04/18
TODO:
    * Logging policy ? => not worth ?
"""

import pygame
import settings.settings as settings
import constants.colors as colors

from modules.managers.InputManager import myInputManager
from modules.managers.GuiManager import myGuiManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.LangManager import myLangManager

from modules.widgets.menu.MainMenu import MainMenu


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
        self._clock = None
        self._debug = settings.DEBUG
        self._managerList = {
            'Game': self,
            'Display': myDisplayManager,
            'Input': myInputManager,
            'Gui': myGuiManager,
            'Lang': myLangManager
        }

        self._scenes = {}
        self._currentScene = None

        self.deltaTime = 0

    def init(self):
        """
        Init pygame and display
        :return: Nothing
        """
        pygame.init()
        self._clock = pygame.time.Clock()
        self._running = True

        self._managerList['Display'].init(self._managerList)

        for (name, manager) in self._managerList.items():
            if name not in ['Game', 'Display']:
                manager.init(self._managerList)

        self._scenes['mainMenu'] = MainMenu()
        self._currentScene = 'mainMenu'

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

    def renderFps(self, deltaTime):
        """
        Render FPS counter
        :param deltaTime: deltaTime
        :return: Nothing
        """
        if self._debug:
            self._managerList['Gui'].writeText(self._clock.get_fps(), 'Arial', 15, colors.RED, (0, 0))

    def mainLoop(self):
        """
        Principal game loop
        :return: Nothing
        """
        while self._running:
            self._clock.tick(settings.FPS)
            self.deltaTime = self._clock.get_time()
            myInputManager.handleEvents([self._scenes[self._currentScene].processEvent])
            myDisplayManager.render([self.renderFps, self._scenes[self._currentScene].render])


myGameManager = GameManager()
