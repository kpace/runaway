from cells import Cell, Hero, Position


class Map:
    PASSABLE = {' ', '.'}

    def __init__(self, file_name):
        self.__load_map(file_name)

    def __load_map(self, file_name):
        self.field = []
        with open(file_name) as file:
            i = 0
            for line in file:  # can be refactored with list comprehension
                l = []
                for j, ch in enumerate(line[:-1]):
                    is_passable = ch in self.PASSABLE
                    if ch == 'H':
                        l.append(
                            Hero(Position(i, j)))
                    else:
                        l.append(Cell(is_passable, ch, Position(i, j)))
                self.field.append(l)
                i += 1
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
        i = position.i
        j = position.j
        if i in range(0, self.height) and j in range(0, self.width):
            return self.field[i][j]

    def __setitem__(self, position, value):
        i = position.i
        j = position.j
        if i in range(0, self.height) and j in range(0, self.width):
            self.field[i][j] = value

    def get_hero(self):
        for line in self.field:
            for x in line:
                if type(x) is Hero:
                    return x
