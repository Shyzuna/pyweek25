"""
Title: Fading text on background widget
Desc: Used for specifics cinematic like intro credits ...
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
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
        self._dialogBackground = pygame.Surface((self._width + (2 * self._padding), self._height + (2 * self._padding)), pygame.SRCALPHA)
        self._dialogBackground.fill(pygame.Color(117, 117, 117, 180))

        self._position = myDisplayManager.getCenterPosition(self._dialogBackground.get_size())

        self._isFading = True
        self._currentFading = 0
        self._fadeDirection = 1
        self._fadeSpeed = 1

        self._resources = {}
        self.loadResources()
        self.renderDialogs()

    def loadResources(self):
        if self._dialogResources:
            for res in self._dialogResources:
                if res['type'] == 'image':
                    try:
                        self._resources[res['id']] = pygame.image.load(os.path.join(settings.IMAGE_PATH, res['name']))
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
                    estimateW, estimateH = myGuiManager.estimateSize(content + ' ' + word, 'Allegro', 20)
                    if estimateW > self._width:
                        subDialog.append(myGuiManager.createText(content, 'Allegro', 20, colors.BLACK))
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
                    subDialog.append(myGuiManager.createText(content, 'Allegro', 20, colors.BLACK))
                    if (len(subDialog) + 1) * estimateH >= self._height:
                        fullDialog.append(subDialog)
                        subDialog = []
            if len(subDialog) > 0:
                fullDialog.append(subDialog)
            self._renderedDialogs.append(fullDialog)

    def refresh(self):
        self.width = 0.8 * myDisplayManager.getSize()[0]
        self.height = 0.6 * myDisplayManager.getSize()[1]
        self._dialogBackground = pygame.Surface((self._width + (2 * self._padding),
                                                 self._height + (2 * self._padding)), pygame.SRCALPHA)
        self._dialogBackground.fill(pygame.Color(117, 117, 117, 180))
        self._position = myDisplayManager.getCenterPosition(self._dialogBackground.get_size())
        self._currentSubDialog = 0
        self._currentDialog = 0
        self._lastDialog = -1
        self.renderDialogs()

    def update(self):
        if self._currentDialog != self._lastDialog:
            for act in self._dialogActions:
                if act['at'] == self._currentDialog:
                    self.processAction(act)

    def processAction(self, action):
        if action['type'] == 'changeBg':
            self._background = self._resources[action['arg']]

    def fade(self, surface):
        self._currentFading += (self._fadeDirection * (self._fadeSpeed * self._myGameManager.deltaTime / 100.0))
        self._currentFading = int(self._currentFading)
        if self._fadeDirection == 1 and self._currentFading > 255:
            self._currentFading = 255
            self._isFading = False
        elif self._fadeDirection == -1 and self._currentFading < 0:
            self._currentFading = 0
            self._isFading = False

        w, h = surface.get_size()
        newSurface = surface.copy().convert_alpha()
        for x in range(w):
            for y in range(h):
                r, g, b, a = surface.get_at((x, y))
                newSurface.set_at((x, y), pygame.Color(r, g, b, self._currentFading))
        return newSurface

    def render(self, deltaTime):
        myDisplayManager.display(self._background, (0, 0))
        myDisplayManager.display(self._dialogBackground, self._position)
        positionT = self._position[0] + self._padding
        positionL = self._position[1] + self._padding
        for dialog in self._renderedDialogs[self._currentDialog][self._currentSubDialog]:
            surface = dialog
            if self._isFading:
                surface = self.fade(surface)
            myDisplayManager.display(surface, (positionT, positionL))
            positionL += dialog.get_size()[1]

    def processEvent(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._currentSubDialog += 1
                if self._currentSubDialog > (len(self._renderedDialogs[self._currentDialog]) - 1):
                    self._currentSubDialog = 0
                    self._currentDialog += 1
                    if self._currentDialog > self._maxDialog:
                        self._myGameManager.previousScene()
