class Map:
    def __init__(self, file_name):
        self.__load_map(file_name)

    def __load_map(self, file_name):
        self.field = []
        with open(file_name) as file:
            y = 0
            for line in file:
                l = []
                for x, ch in enumerate(line):
                    l.append(Cell(self, ch, Position(x, y)))
                self.field.append(l)
                y += 1

    def __str__(self):
        s = ''
        for line in self.field:
            for cell in line:
                s += str(cell)

        return s


class Cell:
    def __init__(self, map, symbol, position):
        self.map = map
        self.symbol = symbol
        self.position = position

    def __str__(self):
        return self.symbol


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
