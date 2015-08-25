from cells import Position
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
        to_move_pos = self.hero.position + direction
        to_move = self.map[to_move_pos]

        if to_move and to_move.passable:
            self.map[to_move_pos] = self.hero
            to_move.position = self.hero.position
            self.map[self.hero.position] = to_move
            self.hero.position = to_move_pos
            return True

    def movement(self):
        while True:
            print(self.map)
            direction = input()
            self.move_hero(direction)
            os.system('clear')
