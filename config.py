""" This file contains different configuration values of the game """

SPEED = 200
CELL_SIZE = 25
WINDOW_OFFSET_X = 450
WINDOW_OFFSET_Y = 150

# override with config_local configurations
try:
    from config_local import *
except ImportError:
    pass