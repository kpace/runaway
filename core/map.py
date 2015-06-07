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
                for x, ch in enumerate(line[:-1]):
                    is_passable = ch in self.PASSABLE
                    if ch == 'H':
                        l.append(Hero(Position(x, y)))
                    else:
                        l.append(Cell(is_passable, ch, Position(x, y)))
                self.field.append(l)
                y += 1
        self.height = len(self.field)
        self.width = len(self.field[0])

    def __str__(self):
        s = ''
        for line in self.field:
            for cell in line:
                s += str(cell)
            s += '\n'

        return s

    def __getitem__(self, position):
        x = position.x
        y = position.y
        if x in range(0, self.width) and y in range(0, self.height):
            return self.field[y][x]

    def __setitem__(self, position, value):
        x = position.x
        y = position.y
        if x in range(0, self.width) and y in range(0, self.height):
            self.field[y][x] = value

    def get_hero(self):
        for line in self.field:
            for x in line:
                if type(x) is Hero:
                    return x


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Position(x, y)

    def __iadd__(self, other):
        """ equivalent to += """
        self.x += other.x
        self.y += other.y

        return self


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
