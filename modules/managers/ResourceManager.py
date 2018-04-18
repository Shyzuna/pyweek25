"""
Title: ResourceManager
Desc: Cache all loaded resources (especially images)
Creation: 18/04/18
Last Mod: 18/04/18
TODO:
"""
# coding=utf-8
import pygame


class ResourceManager(object):
    def __init__(self):
        self._caches = {}
        self._acceptedType = ['image']
        self._managerList = None
        self._init = False

    def init(self, managerList):
        self._managerList = managerList
        for elemType in self._acceptedType:
            self._caches[elemType] = {}
        self._init = True

    def loadResource(self, elemId, elemType, elemPath, arg):
        if elemType == 'image':
            if arg:
                self._caches['image'][elemId] = pygame.image.load(elemPath).convert_alpha()
            else:
                self._caches['image'][elemId] = pygame.image.load(elemPath).convert()
            return self._caches['image'][elemId]

    def lookFor(self, elemId, elemType, elemPath, arg):
        if elemType in self._acceptedType:
            if elemId in self._caches[elemType].keys():
                return self._caches[elemType][elemId]
            return self.loadResource(elemId, elemType, elemPath, arg)
        else:
            print("[ResourceManager] - Invalid resource type : " + elemType)


myResourceManager = ResourceManager()
