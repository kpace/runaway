class Cell:
    def __init__(self, passable=True, symbol=' '):
        self.passable = passable
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Hero(Cell):
    def __init__(self, lives=3):
        super().__init__(False, 'H')
        self.lives = lives


# class Position:
#     def __init__(self, i, j):
#         self.i = i
#         self.j = j
#
#     def __add__(self, other):
#         i = self.i + other.i
#         j = self.j + other.j
#
#         return Position(i, j)
#
#     def __iadd__(self, other):
#         """ equivalent to += """
#         self.i += other.i
#         self.j += other.j
#
#         return self
