import pygame as pg
import pygame_gui as gui

RESOLUTION = WIDTH, HEIGHT = 1280, 720

TITLE = 'Stray Cat'
GAME_NAME = 'STRAY CAT'

MENU_BG_IMG = 'assets/img/bg/menu.jpg'

DEFAULT_TEXT_FONT = "assets/font/DFVN Boris.otf"

###############################################
# ########## Text and Dialogue #################
TEXT_BOX_IMG = 'assets/img/gui/textbox.png'
MESSAGE_LINE_IMG = 'assets/img/gui/message_line.png'

DIALOGUE_FONT_SIZE = 25
DIALOGUE_TEXT_COLOR = (255, 255, 255)

################################################
WHACK_WIN_SCORE = 10

################################################
CHARACTER_DIALOGUE = {
    "cat": {
        'default': "",
    },
    "bot": {
        'default': ""
    }
}

################################################
CACHE = {
    'flappy_cat': {
        'obstacle': {
            0: 'assets/img/flappy_cat/0.png',
            1: 'assets/img/flappy_cat/1.png',
            2: 'assets/img/flappy_cat/2.png',
            3: 'assets/img/flappy_cat/3.png',
        },
        'portal': {
            'path': 'assets/img/flappy_cat/portal.png',
            'num_frames': 24
        },
        'cat': {
            'path': 'assets/img/flappy_cat/cat.png'
        }
    },
    'loading': {
        'path': 'assets/img/gui/loading.png',
        'num_frames': 30
    },
    'cat': {
        'idle': {
            'path': 'assets/img/cat/Cat-1-Idle.png',
            'num_frames': 10,
            'scale': 7,
        },
        'walk': {
            'path': 'assets/img/cat/Cat-1-Walk.png',
            'num_frames': 8,
            'scale': 7,
        },
        'jump': {
            'path': 'assets/img/cat/Cat-1-Run.png',
            'num_frames': 8,
            'scale': 7,
        },
        'meow': {
            'path': 'assets/img/Cat/Cat-1-Meow.png',
            'num_frames': 4,
            'scale': 7,
        }
    },
    'bot': {
        'idle': {
            'path': 'assets/img/bot/idle.png',
        },
        'left': {
            'path': 'assets/img/bot/left.png',
        },
        'right': {
            'path': 'assets/img/bot/right.png',
        }
    }
}