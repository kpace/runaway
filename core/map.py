class Map:
    PASSABLE = {' ', '.'}

    def __init__(self, file_name):
        self.__load_map(file_name)

    def __load_map(self, file_name):
        self.field = []
        with open(file_name) as file:
            y = 0
            for line in file: # can be refactored with list comprehention
                l = []
                for x, ch in enumerate(line):
                    is_passable = ch in self.PASSABLE
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
    def __init__(self, is_passable, symbol, position):
        self.is_passable = is_passable
        self.symbol = symbol
        self.position = position

    def __str__(self):
        return self.symbol


map = Map("../static/maps/m1.txt")
print(map[(1, 1)].is_passable)