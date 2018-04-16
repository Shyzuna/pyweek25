"""
Title: Main menu
Desc: Display and handle events for mainMenu
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
"""

# coding=utf-8

import pygame

import settings.settings as settings
import constants.colors as colors
from modules.widgets.menu.TextButton import TextButton
from modules.managers.LangManager import myLangManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.GuiManager import myGuiManager


class MainMenu(object):
    """
    MainMenu
    """
    def __init__(self, myGameManager):
        """
        Create basic button and state for the menu
        """
        self._myGameManager = myGameManager
        self._buttonsLabels = ['menu.play', 'menu.options', 'menu.credits', 'menu.exit']
        self._titleSurface = myGuiManager.createText(settings.TITLE, 'Allegro', 38, colors.BLACK)
        self._buttons = []
        self._selectedButton = 0
        self._margin = 15.0
        self.createButtons()

    def buttonsHandler(self):
        if self._selectedButton == 0:
            self._myGameManager.changeCurrentScene('intro')
        elif self._selectedButton == 1:
            self._myGameManager.changeCurrentScene('optionsMenu')
        elif self._selectedButton == 2:
            pass
        elif self._selectedButton == 3:
            self._myGameManager.stop()

    def createButtons(self):
        self._buttons.clear()
        screenW, screenH = myDisplayManager.getSize()
        positionT = 0.15 * screenW
        positionL = 0
        index = 0
        for label in self._buttonsLabels:
            if index > 0:
                positionT += self._buttons[index-1].getSizes()[1] + self._margin
            self._buttons.append(
                TextButton(myLangManager.getLabel(label), 'Allegro', 32, colors.BLACK,
                           (positionL, positionT), self._selectedButton == index)
            )
            if index == 0:
                # Button all same width
                positionL = myDisplayManager.getCenterPosition(self._buttons[0].getSizes())[0]
                self._buttons[0].setPosition((positionL, positionT))
            index += 1

    def refresh(self):
        self.createButtons()

    def update(self):
        pass

    def render(self, deltaTime):
        titlePosition = (myDisplayManager.getCenterPosition(self._titleSurface.get_size())[0], self._margin)
        myDisplayManager.display(self._titleSurface, titlePosition)
        index = 0
        for button in self._buttons:
            button.setShaking(self._selectedButton == index)
            button.renderButton(deltaTime)
            index += 1

    def processEvent(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self._selectedButton -= 1
                self._selectedButton = (len(self._buttons) - 1) if self._selectedButton < 0 else self._selectedButton
            if event.key == pygame.K_DOWN:
                self._selectedButton += 1
                self._selectedButton = 0 if self._selectedButton > (len(self._buttons) - 1) else self._selectedButton
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.buttonsHandler()