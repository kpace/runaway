from cells import Hero

class GameManager:
    def __init__(self, map):
        self.map = map
        self.hero = self.get_hero()
        self.hero_position = self.get_hero_position()

    def move_hero(self, direction):
        to_move_pos = tuple(map(sum, zip(self.hero_position, direction)))
        to_move = self.map[to_move_pos]

        if to_move and to_move.passable:
            self.map[to_move_pos] = self.hero
            to_move.position = self.hero_position
            self.map[self.hero_position] = to_move
            self.hero_position = to_move_pos
            return True

        return False

    def get_hero(self):
        #TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return x

    def get_hero_position(self):
        #TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return i, j

    def dimensions(self):
        return self.map.height, self.map.width

    def symbol_at(self, position):
        return self.map[position].symbol
