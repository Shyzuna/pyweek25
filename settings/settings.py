"""
Title: Settings
Desc: Contains settings for program execution
Creation: 15/04/18
Last Mod: 15/04/18
TODO: /
"""

# coding=utf-8

import os


# Display:
DEFAULT_RESOLUTION = 0
FPS = 60
FULL_SCREEN = False
AVAILABLE_RESOLUTION = [
    (800, 600),
    (1200, 800),
    (1600, 900),
    (1920, 1080)
]

# Path
IMAGE_PATH = os.path.join('data', 'images')
LANGS_PATH = os.path.join('data', 'langs')
DIALOGS_PATH = os.path.join('data', 'dialogs')

# Lang
DEFAULT_LANG = 'en'
LANG_LIST = ['en', 'fr']

# Misc
DEBUG = True
TITLE = 'I need a title - Pyweek#25'
