from map import Position
import os

DIRECTIONS = {
    'l': Position(-1, 0),
    'r': Position(1, 0),
    'u': Position(0, -1),
    'd': Position(0, 1)
}


class GameManager:
    def __init__(self, map):
        self.map = map
        self.hero = map.get_hero()

    def move_hero(self, direction):
        pos = self.hero.position + DIRECTIONS[direction]
        to_move = self.map[pos]

        if to_move and to_move.passable:
            self.map[pos] = self.hero
            to_move.position = self.hero.position
            self.map[to_move.position] = to_move
            self.hero.position = pos

    def movement(self):
        while True:
            print(self.map)
            direction = input()
            self.move_hero(direction)
            os.system('clear')

