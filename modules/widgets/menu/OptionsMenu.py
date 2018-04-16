"""
Title: Options menu
Desc: Display and handle events for optionsMenu
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
    * Could merge with MainMenu
"""

# coding=utf-8

import pygame

import settings.settings as settings
import constants.colors as colors
from modules.widgets.menu.TextButton import TextButton
from modules.managers.LangManager import myLangManager
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.GuiManager import myGuiManager


class OptionsMenu(object):
    """
    OptionsMenu
    """
    def __init__(self, myGameManager):
        """
        Create basic button and state for the menu
        """
        self._myGameManager = myGameManager
        self._buttonsLabels = ['options.screen-size', 'options.fullscreen', 'options.language', 'options.return']
        self._titleSurface = myGuiManager.createText(myLangManager.getLabel('menu.options'),
                                                     'Allegro', 38, colors.BLACK)
        self._buttons = []
        self._selectedButton = 0
        self._margin = 15.0
        self.createButtons()

    def createOptionsLabel(self, label):
        value = myLangManager.getLabel(label)
        if label == 'options.screen-size':
            value += ' : ' + str(myDisplayManager.getSize()[0]) + 'x' + str(myDisplayManager.getSize()[1])
        elif label == 'options.fullscreen':
            value += ' : ' + ('On' if myDisplayManager.isFullscreen() else 'Off')
        elif label == 'options.language':
            value += ' : ' + myLangManager.getCurrentLang()
        return value

    def buttonsHandler(self):
        if self._selectedButton == 0:
            myDisplayManager.nextResolution()
        elif self._selectedButton == 1:
            myDisplayManager.toggleFullScreen()
        elif self._selectedButton == 2:
            myLangManager.nextLanguage()
        elif self._selectedButton == 3:
            self._myGameManager.previousScene()
        self.createButtons()

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
                TextButton(self.createOptionsLabel(label), 'Allegro', 32, colors.BLACK,
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
