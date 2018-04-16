"""
Title: LangManager
Desc: Handle language modification for dialogs and labels
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
"""
# coding=utf-8

import json
import codecs
import os
import settings.settings as settings


class LangManager(object):
    """
        DisplayManager class
    """
    def __init__(self):
        """
            Init base elements
        """
        self._init = False
        self._managerList = None
        self._labels = {}
        self._dialogs = {}
        self._currentLang = None
        self._langList = []

    def init(self, managerList):
        """
        Init languages files and dialogs
        :return: Nothing
        """
        self._managerList = managerList
        self._currentLang = settings.DEFAULT_LANG
        self._langList = settings.LANG_LIST
        for lang in settings.LANG_LIST:
            try:
                with open(os.path.join(settings.LANGS_PATH, lang, 'data.json'), 'rb') as file:
                    data = file.read().decode('utf-8')
                    langsData = json.loads(data)
                    self._labels[lang] = langsData
            except Exception as e:
                print("[LangManager] - Could'nt load language : " + lang)
                raise e
                print(e)

    def getLabel(self, path):
        elements = path.split('.')
        currentLabel = self._labels[self._currentLang]
        for elem in elements:
            if elem not in currentLabel.keys():
                print("[LangManager] - Could'nt find label")
                return None
            currentLabel = currentLabel[elem]
        return currentLabel

    def getCurrentLang(self):
        return self._currentLang

    def nextLanguage(self):
        index = self._langList.index(self._currentLang) + 1
        index = 0 if index > len(self._langList) - 1 else index
        self._currentLang = self._langList[index]


myLangManager = LangManager()
