"""
Title: Text Button Widget
Desc: Button element for menus
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
    * Load images smw else ?
    * Add anchor ?
    * Parenting positioning ?
"""

# coding=utf-8

import pygame
import os

from modules.managers.GuiManager import myGuiManager
from modules.managers.DisplayManager import myDisplayManager
import settings.settings as settings


class TextButton(object):
    """
    TextButton
    """
    def __init__(self, text, font, size, color, position=(0, 0), shaking=False):
        """
        Create a textual button
        :param text:
        :param font:
        :param size:
        :param color:
        :param position:
        """
        self._textSurface = myGuiManager.createText(text, font, size, color)
        print(text)
        self._buttonImg = pygame.image.load(os.path.join(settings.IMAGE_PATH, 'button.png'))
        self._position = position

        self._shaking = shaking
        self._maxShacking = 10.0
        self._shakingPerS = 6.0
        self._shakingDirection = 1
        self._currentShaking = 0.0

    def getSizes(self):
        return self._buttonImg.get_size()

    def setPosition(self, position):
        self._position = position

    def setShaking(self, shake):
        self._shaking = shake

    def shake(self, position, deltaTime):
        """
        Make the button shake up/down is shaking enable
        :param position: base position
        :param deltaTime: deltaTime
        :return: new position
        """
        height = position[1]
        if self._shaking:
            self._currentShaking += self._shakingDirection * (self._shakingPerS * deltaTime / 100.0)
            if self._shakingDirection == 1 and self._currentShaking >= self._maxShacking:
                self._currentShaking = self._maxShacking
                self._shakingDirection = -1
            elif self._shakingDirection == -1 and self._currentShaking <= (-1 * self._maxShacking):
                self._currentShaking = -1 * self._maxShacking
                self._shakingDirection = 1
            height += self._currentShaking
        return position[0], height

    def renderButton(self, deltaTime, position=None):
        """
        Display the button
        :param position: if no position use default
        :return: Nothing
        """
        currentPosition = position if position else self._position
        currentPosition = self.shake(currentPosition, deltaTime)

        buttonSize = self._buttonImg.get_size()
        textSize = self._textSurface.get_size()

        textPosition = ((buttonSize[0] - textSize[0]) / 2 + currentPosition[0],
                        (buttonSize[1] - textSize[1]) / 2 + currentPosition[1])

        myDisplayManager.display(self._buttonImg, currentPosition)
        myDisplayManager.display(self._textSurface, textPosition)
