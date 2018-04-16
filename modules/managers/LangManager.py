"""
Title: LangManager
Desc: Handle language modification for dialogs and labels
Creation: 16/04/18
Last Mod: 16/04/18
TODO:
"""
import json
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

    def init(self, managerList):
        """
        Init languages files and dialogs
        :return: Nothing
        """
        self._managerList = managerList
        self._currentLang = settings.DEFAULT_LANG
        for lang in settings.LANG_LIST:
            try:
                langsData = json.load(open(os.path.join(settings.LANGS_PATH, lang, 'data.json')))
                self._labels[lang] = langsData
            except Exception as e:
                print("[LangManager] - Could'nt load language : " + lang)
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


myLangManager = LangManager()
