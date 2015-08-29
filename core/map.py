from cells import Cell, Hero


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
                            Hero())
                    else:
                        l.append(Cell(is_passable, ch))
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
            return self.field[position[0]][position[1]]

    def __setitem__(self, position, value):
        self.field[position[0]][position[1]] = value

