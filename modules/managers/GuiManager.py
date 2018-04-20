"""
Title: GuiManager
Desc: Display the menu and user interfaces elements
Creation: 15/04/18
Last Mod: 15/04/18
TODO:
    * regroup gui element for less functions
"""

# coding=utf-8

import constants.colors as colors
import pygame
import os
import settings.settings as settings
from modules.widgets.dialog.DialogHandler import DialogHandler


class GuiManager(object):
    def __init__(self):
        self._fontList = {}
        self._defaultSize = (1920, 1080)
        self._defaultFontSize = [20, 25, 30, 35]
        self._managerList = None
        self._init = False
        self._guiElements = None
        self._toolTipText = []
        self._toolTipPosition = None
        self._selectorContent = []
        self._selectorPosition = None
        self._selectedContent = []
        self._selectedPosition = None
        self._guiEnable = False

    def init(self, managerList):
        self._managerList = managerList
        self.refresh()
        self._init = True

    def loadFont(self, name, size, sysFont=True):
        fontFullName = name + '-' + str(size)
        if fontFullName not in self._fontList.keys():
            if sysFont:
                self._fontList[fontFullName] = pygame.font.SysFont(name, size)
            else:
                self._fontList[fontFullName] = pygame.font.Font(os.path.join(settings.FONT_PATH, name + '.ttf'), size)
        return fontFullName

    def createText(self, text, font, size, color, antiAliased=True, sysFont=True):
        fontFullName = self.loadFont(font, size, sysFont)
        return self._fontList[fontFullName].render(str(text), antiAliased, color)

    def writeText(self, text, font, size, color, position):
        label = self.createText(text, font, size, color)
        self._managerList['Display'].display(label, position)

    def estimateSize(self, text, font, size, sysFont=True):
        fontFullName = self.loadFont(font, size, sysFont)
        return self._fontList[fontFullName].size(text)

    def setTooltip(self, text):
        if text:
            self._toolTipText.clear()
            elems = text.split('|')
            for elem in elems:
                self._toolTipText.append(self.createText(elem, 'Lucida Console', 20, colors.RED, False))
        else:
            self._toolTipText = []

    def setSelectorContent(self, text):
        if text:
            self._selectorContent.clear()
            elems = text.split('|')
            for elem in elems:
                self._selectorContent.append(self.createText(elem, 'Lucida Console', 20, colors.RED, False))
        else:
            self._selectorContent = []

    def setPersonSelectorContent(self, text, charInfo):
        text += '|Hp: ' + str(charInfo['hp']) + '|Mp: ' + str(charInfo['mp'])
        self.setSelectorContent(text)

    def setSelectedContent(self, text):
        if text:
            self._selectedContent.clear()
            elems = text.split('|')
            for elem in elems:
                self._selectedContent.append(self.createText(elem, 'Lucida Console', 20, colors.RED, False))
        else:
            self._selectedContent = []

    def setPersonSelectedContent(self, text, charInfo):
        text += '|Hp: ' + str(charInfo['hp']) + '|Mp: ' + str(charInfo['mp'])
        self.setSelectedContent(text)


    def refresh(self):
        screenW, screenH = self._managerList['Display'].getSize()

        rescaleX, rescaleY = screenW / self._defaultSize[0], screenH / self._defaultSize[1]
        currentRes = self._managerList['Display'].getResolutionNumber()

        self._toolTipPosition = (0.05 * screenW, 0.9 * screenH)
        self._selectorPosition = (0.8 * screenW, 0.9 * screenH)
        self._selectedPosition = (0.05 * screenW, 0.05 * screenH)

        defaultBox = self._managerList['Resource'].lookFor('box', 'image', os.path.join(settings.IMAGE_PATH, 'box.png'), True)
        boxSize = defaultBox.get_size()
        newSize = (int(boxSize[0] * rescaleX), int(boxSize[1] * rescaleY))
        paddingX, paddingY = 0.05 * newSize[0], 0.10 * newSize[1]
        dialogBoxPos = 0.05 * screenW, screenH - newSize[1] - 0.05 * screenH
        dialog = DialogHandler(self, 'dialog1', (newSize[0] - 2 * paddingX, newSize[1] - 2 * paddingY),
                               (dialogBoxPos[0] + paddingX, dialogBoxPos[1] + paddingY),
                               self._defaultFontSize[currentRes], True)

        self._guiElements = {
            'dialogBox': {
                'active': False,
                'position': dialogBoxPos,
                'background': pygame.transform.scale(defaultBox, newSize),
                'content': dialog
            }
        }

    def update(self, deltaTime):
        if not self._guiEnable:
            return

        for key, elem in self._guiElements.items():
            if elem['active']:
                elem['content'].update(deltaTime)

    def stopGuiElement(self, element):
        self._guiElements[element]['active'] = False

    def processEvents(self, event):
        if not self._guiEnable:
            return

        for key, elem in self._guiElements.items():
            if elem['active']:
                if elem['content'].processEvent(event):
                    return

    def toggleGui(self):
        self._guiEnable = not self._guiEnable

    def render(self, deltaTime):
        if not self._guiEnable:
            return

        if len(self._toolTipText) > 0:
            xPos, yPos = self._toolTipPosition
            for text in self._toolTipText:
                self._managerList['Display'].display(text, (xPos, yPos))
                yPos += text.get_size()[1] + 5
        if len(self._selectorContent) > 0:
            xPos, yPos = self._selectorPosition
            for text in self._selectorContent:
                self._managerList['Display'].display(text, (xPos, yPos))
                yPos += text.get_size()[1] + 5
        if len(self._selectedContent) > 0:
            xPos, yPos = self._selectedPosition
            for text in self._selectedContent:
                self._managerList['Display'].display(text, (xPos, yPos))
                yPos += text.get_size()[1] + 5

        for key, elem in self._guiElements.items():
            if elem['active']:
                self._managerList['Display'].display(elem['background'], elem['position'])
                elem['content'].render(deltaTime)


myGuiManager = GuiManager()

