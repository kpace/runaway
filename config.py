""" This file contains different configuration values of the game """
import os

HERO_MOVEMENT_SPEED = 200
MONSTER_MOVEMENT_SPEED = 250
CHASE_WANDER_SPEED = 4000
CELL_SIZE = 25
WINDOW_OFFSET_X = 450
WINDOW_OFFSET_Y = 150

PROJECT_ROOT = os.path.dirname(__file__)

# override with config_local configurations
try:
    from config_local import *
except ImportError:
    pass