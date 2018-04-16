"""
Title: Settings
Desc: Contains settings for program execution
Creation: 15/04/18
Last Mod: 15/04/18
TODO: /
"""
import os


# Display:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FULL_SCREEN = False

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
