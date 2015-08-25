class Cell:
    def __init__(self, passable, symbol, position):
        self.passable = passable
        self.symbol = symbol
        self.position = position

    def __str__(self):
        return self.symbol


class Hero(Cell):
    def __init__(self, position, lives=3):
        super().__init__(False, 'H', position)
        self.lives = lives


class Position:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        i = self.i + other.i
        j = self.j + other.j

        return Position(i, j)

    def __iadd__(self, other):
        """ equivalent to += """
        self.i += other.i
        self.j += other.j

        return self
