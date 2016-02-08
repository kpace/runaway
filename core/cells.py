class Cell:
    def __init__(self, x, y, passable=True, symbol=' '):
        self.x = x
        self.y = y
        self.passable = passable
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __lt__(self, other):
        return True

class Hero(Cell):
    def __init__(self, x, y, lives=3):
        super().__init__(x, y, True, 'H')
        self.lives = lives


class Monster(Cell):
    def __init__(self, x, y):
        super().__init__(x, y, False, '$')
        self.path = []



