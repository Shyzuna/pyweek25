"""
Title: InputManager
Desc: Handles input from player
Creation: 15/04/18
Last Mod: 16/04/18
TODO:
"""

# coding=utf-8

import pygame


class InputManager(object):
    def __init__(self):
        self._managerList = None
        self._init = False

    def init(self, managerList):
        self._managerList = managerList
        self._init = True

    def handleEvents(self, eventHandlers):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._managerList['Game'].stop()
            for eventHandler in eventHandlers:
                eventHandler(event)


myInputManager = InputManager()
