from core.cells import Cell, Hero, Monster


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
                    if ch == 'H':
                        l.append(Hero(i, j))
                    elif ch == '$':
                        l.append(Monster(i, j))
                    else:
                        is_passable = ch in self.PASSABLE
                        l.append(Cell(i, j, is_passable, ch))
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

    def neighbours(self, cell):
        # TODO: think about refactoring this
        neighbours = []
        neighbours.append(self.field[cell.y - 1][cell.x])
        neighbours.append(self.field[cell.y][cell.x + 1])
        neighbours.append(self.field[cell.y + 1][cell.x])
        neighbours.append(self.field[cell.y][cell.x - 1])

        return neighbours

    def dist_between(self, cell1, cell2):
        return abs(cell1.y - cell2.y) + abs((cell1.x - cell2.x))

    def swap_cells(self, c1, c2):
        c1_pos = c1.y, c1.x
        c2_pos = c2.y, c2.x

        tmp = c1
        self[c1_pos] = c2
        self[c2_pos] = tmp

        c1.y, c1.x = c2_pos
        c2.y, c2.x = c1_pos
