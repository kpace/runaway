class Cell:
    def __init__(self, y, x, passable=True, symbol=' '):
        self.y = y
        self.x = x
        self.passable = passable
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.passable == other.passable and self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + self.symbol)


class Hero(Cell):
    def __init__(self, y, x, lives=3):
        super().__init__(y, x, True, 'H')
        self.lives = lives


class Monster(Cell):
    def __init__(self, y, x):
        super().__init__(y, x, False, '$')
        self.path = []



