class Cell:
    def __init__(self, pos, passable=True, symbol=' '):
        self.position = pos
        self.passable = passable
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self.position == other.position and \
               self.passable == other.passable and self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self.position.x) + str(self.position.y) + self.symbol)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

class Hero(Cell):
    def __init__(self, pos, lives=3):
        super().__init__(pos, True, 'H')
        self.lives = lives


class Monster(Cell):
    def __init__(self, pos, direction, chasing=True):
        super().__init__(pos, False, '$')
        self.chasing = chasing
        self.direction = direction
        self.path = []


class Position:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __add__(self, other):
        return Position(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Position(self.y - other.y, self.x - other.x)


class Direction:
    UP = Position(-1, 0)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)
    RIGHT = Position(0, 1)
