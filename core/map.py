class Map:
    PASSABLE = {' ', '.'}

    def __init__(self, file_name):
        self.__load_map(file_name)

    def __load_map(self, file_name):
        self.field = []
        with open(file_name) as file:
            y = 0
            for line in file:  # can be refactored with list comprehension
                l = []
                for x, ch in enumerate(line):
                    is_passable = ch in self.PASSABLE
                    if ch == 'H':
                        l.append(Hero((x, y)))
                    else:
                        l.append(Cell(is_passable, ch, (x, y)))
                self.field.append(l)
                y += 1

    def __str__(self):
        s = ''
        for line in self.field:
            for cell in line:
                s += str(cell)

        return s

    def __getitem__(self, position):
        return self.field[position[1]][position[0]]


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

m = Map('../static/maps/m1.txt')
print(m)