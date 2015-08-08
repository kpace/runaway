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