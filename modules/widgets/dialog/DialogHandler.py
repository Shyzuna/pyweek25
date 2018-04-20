"""
Title: DialogHandler
Desc: widget to handle dialogs
Creation: 20/04/18
Last Mod: 20/04/18
TODO:
    * Should not redraw if not letterbyletter
"""
# coding=utf-8

import os
import pygame
import math
from modules.managers.DisplayManager import myDisplayManager
from modules.managers.ResourceManager import myResourceManager
from modules.managers.LangManager import myLangManager
import settings.settings as settings
import constants.colors as colors


class DialogHandler(object):
    def __init__(self, myGuiManager, dialog, textWindow, textPosition, fontSize, letterByLetter=False):
        self._myGuiManager = myGuiManager
        self._dialogData = myLangManager.getDialog(dialog)
        self._position = textPosition
        self._width, self._height = textWindow
        self._lineSpace = 0.02 * self._height

        self._fontSize = fontSize
        self._dialogText = self._dialogData['dialogs']
        self._dialogSpeaker = self._dialogData['speakers']
        self._letterByLetter = letterByLetter
        self._effect = letterByLetter
        self._textSurface = pygame.Surface(textWindow, pygame.SRCALPHA)
        self._textSurface.fill((0, 0, 0, 0))

        self._letterFrequency = 2
        self._currentLetter = 0
        self._letterForBlock = 0
        self._preparedDialogs = []

        self._currentDialog = 0
        self._currentSubDialog = 0
        self.prepareDialogs()

    def prepareDialogs(self):
        self._preparedDialogs.clear()
        index = 0
        for dialog in self._dialogText:
            fullDialog = []
            subDialog = []
            lines = dialog.split('\n')
            for line in lines:
                words = line.split(' ')
                if len(subDialog) == 0:
                    content = self._dialogSpeaker[index] + ' :'
                else:
                    content = ""
                for word in words:
                    estimateW, estimateH = self._myGuiManager.estimateSize(content + ' ' + word, 'alterebro-pixel-font',
                                                                     self._fontSize, False)
                    if estimateW > self._width:
                        subDialog.append(content)
                        if (len(subDialog) + 1) * estimateH >= (self._height - (len(subDialog) * self._lineSpace)):
                            fullDialog.append(subDialog)
                            subDialog = []
                        content = word
                    else:
                        if len(content) > 0:
                            content += ' ' + word
                        else:
                            content = word
                if len(content) > 0:
                    subDialog.append(content)
                    if (len(subDialog) + 1) * estimateH >= (self._height - (len(subDialog) * self._lineSpace)):
                        fullDialog.append(subDialog)
                        subDialog = []
            if len(subDialog) > 0:
                fullDialog.append(subDialog)
            self._preparedDialogs.append(fullDialog)
            index += 1
        self._letterForBlock = self.getMaxLetterForCurrentBlock()

    def getMaxLetterForCurrentBlock(self):
        size = 0
        for text in self._preparedDialogs[self._currentDialog][self._currentSubDialog]:
            size += len(text)
        return size

    def renderCurrentSubBlock(self):
        self._textSurface.fill((0, 0, 0, 0))
        positionT = 0
        positionL = 0
        letterNumber = math.floor(self._currentLetter)
        for text in self._preparedDialogs[self._currentDialog][self._currentSubDialog]:
            textLen = len(text)
            if letterNumber > textLen:
                letterNumber -= textLen
                currentText = self._myGuiManager.createText(text, 'alterebro-pixel-font', self._fontSize, colors.BLACK,
                                                            False, False)
                self._textSurface.blit(currentText, (positionL, positionT))
            else:
                currentText = self._myGuiManager.createText(text[:letterNumber], 'alterebro-pixel-font', self._fontSize,
                                                            colors.BLACK, False, False)
                self._textSurface.blit(currentText, (positionL, positionT))
                return  # end no letter
            positionT += (self._lineSpace + currentText.get_size()[1])

    def init(self):
        pass

    def refresh(self):
        pass

    def render(self, deltaTime):
        self.renderCurrentSubBlock()
        myDisplayManager.display(self._textSurface, self._position)

    def update(self, deltaTime):
        if self._letterByLetter and self._effect:
            self._currentLetter += self._letterFrequency * deltaTime / 100.0
            if self._currentLetter> self._letterForBlock:
                self._effect = False
                self._currentLetter = self._letterForBlock

    def processEvent(self, event):
        if event.type == pygame.KEYUP and pygame.K_SPACE:
            if self._effect:
                self._effect = False
                self._currentLetter = self._letterForBlock
            else:
                self._currentSubDialog += 1
                if self._currentSubDialog >= len(self._preparedDialogs[self._currentDialog]):
                    self._currentSubDialog = 0
                    self._currentDialog += 1
                    if self._currentDialog >= len(self._preparedDialogs):
                        self._myGuiManager.stopGuiElement('dialogBox')
                        return
                    self._letterForBlock = self.getMaxLetterForCurrentBlock()
                    self._currentLetter = 0 if self._letterByLetter else self._letterForBlock
                    self._effect = True
        return True  # deny all events propagation
