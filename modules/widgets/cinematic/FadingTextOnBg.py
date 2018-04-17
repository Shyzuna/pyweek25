"""
Title: Fading text on background widget
Desc: Used for specifics cinematic like intro credits ...
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
    * Fix Fade bug
    * Make fade out with next dialog
    * resize bg
"""
import pygame
import os

import constants.colors as colors
import settings.settings as settings
from modules.managers.LangManager import myLangManager
from modules.managers.GuiManager import myGuiManager
from modules.managers.DisplayManager import myDisplayManager


class FadingTextOnBg(object):
    def __init__(self, dialog, myGameManager):
        self._myGameManager = myGameManager
        self._dialog = dialog
        data = myLangManager.getDialog(dialog)
        self._renderedDialogs = []
        self._dialogTexts = data['dialogs']
        self._dialogActions = data['actions']
        self._dialogResources = data['resources']
        self._currentSubDialog = 0
        self._currentDialog = 0
        self._lastDialog = -1
        self._maxDialog = len(self._dialogTexts) - 1
        self._background = pygame.Surface(myDisplayManager.getSize())

        self._width = 0.8 * myDisplayManager.getSize()[0]
        self._height = 0.6 * myDisplayManager.getSize()[1]

        self._padding = 20
        self._dialogBackground = pygame.Surface((self._width + (2 * self._padding), self._height + (2 * self._padding)),
                                                pygame.SRCALPHA)
        self._dialogBackground.fill((117, 117, 117, 180))

        self._position = myDisplayManager.getCenterPosition(self._dialogBackground.get_size())

        self._isFading = True
        self._currentFading = 0
        self._fadeDirection = 1
        self._fadeSpeed = 15

        self._resources = {}
        self.loadResources()
        self.renderDialogs()

    def loadResources(self):
        if self._dialogResources:
            for res in self._dialogResources:
                if res['type'] == 'image':
                    try:
                        self._resources[res['id']] = pygame.image.load(os.path.join(settings.IMAGE_PATH, res['name']))\
                            .convert()
                    except Exception as e:
                        print('[FadingTextOnBg] - Error while loading resources')
                        print(e)

    def renderDialogs(self):
        self._renderedDialogs.clear()
        for dialog in self._dialogTexts:
            fullDialog = []
            subDialog = []
            lines = dialog.split('\n')
            for line in lines:
                words = line.split(' ')
                content = ""
                for word in words:
                    estimateW, estimateH = myGuiManager.estimateSize(content + ' ' + word, 'Lucida Console', 20)
                    if estimateW > self._width:
                        subDialog.append(myGuiManager.createText(content, 'Lucida Console', 20, colors.BLACK, False))
                        if (len(subDialog) + 1) * estimateH >= self._height:
                            fullDialog.append(subDialog)
                            subDialog = []
                        content = word
                    else:
                        if len(content) > 0:
                            content += ' ' + word
                        else:
                            content = word
                if len(content) > 0:
                    subDialog.append(myGuiManager.createText(content, 'Lucida Console', 20, colors.BLACK, False))
                    if (len(subDialog) + 1) * estimateH >= self._height:
                        fullDialog.append(subDialog)
                        subDialog = []
            if len(subDialog) > 0:
                fullDialog.append(subDialog)
            self._renderedDialogs.append(fullDialog)

    def refresh(self):
        self._width = 0.8 * myDisplayManager.getSize()[0]
        self._height = 0.6 * myDisplayManager.getSize()[1]
        self._dialogBackground = pygame.Surface((self._width + (2 * self._padding),
                                                 self._height + (2 * self._padding)), pygame.SRCALPHA)
        self._dialogBackground.fill((117, 117, 117, 180))
        self._position = myDisplayManager.getCenterPosition(self._dialogBackground.get_size())
        self._currentSubDialog = 0
        self._currentDialog = 0
        self._lastDialog = -1
        self.renderDialogs()

    def update(self):
        if self._currentDialog != self._lastDialog:
            self._lastDialog = self._currentDialog
            for act in self._dialogActions:
                if act['at'] == self._currentDialog:
                    self.processAction(act)
        if self._isFading:
            self.fade(self._myGameManager.deltaTime)

    def processAction(self, action):
        if action['type'] == 'changeBg':
            self._background = self._resources[action['arg']]

    def fade(self, deltaTime):
        self._currentFading += (self._fadeSpeed * deltaTime / 100) * self._fadeDirection
        if self._fadeDirection == 1 and self._currentFading > 255:  # Fade in
            self._currentFading = 255
            self._isFading = False
        if self._fadeDirection == -1 and self._currentFading < 0:  # Fade out
            self._currentFading = 0
            # Launch next dialog
            self.nextDialog()
            self._fadeDirection = 1

    def nextDialog(self):
        self._currentSubDialog += 1
        if self._currentSubDialog > (len(self._renderedDialogs[self._currentDialog]) - 1):
            self._currentSubDialog = 0
            self._currentDialog += 1
            if self._currentDialog > self._maxDialog:
                self._myGameManager.changeCurrentScene('labo')

    def render(self, deltaTime):
        myDisplayManager.display(self._background, (0, 0))
        myDisplayManager.display(self._dialogBackground, self._position)
        positionT = self._position[0] + self._padding
        positionL = self._position[1] + self._padding
        for dialog in self._renderedDialogs[self._currentDialog][self._currentSubDialog]:
            dialog.set_alpha(self._currentFading)
            myDisplayManager.display(dialog, (positionT, positionL))
            positionL += dialog.get_size()[1]

    def processEvent(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self._isFading:
                    self._isFading = False
                    self._currentFading = 255
                    if self._fadeDirection == -1:
                        self.nextDialog()
                else:
                    self._isFading = True
                    self._fadeDirection = -1
