import random

from core.cells import Cell, Hero, Monster, Position, Direction


class Map:
    PASSABLE = {' ', '.'}

    def __init__(self, file_name):
        self.file_name = file_name
        self.__load_map()

    def __load_map(self):
        self.field = []
        with open(self.file_name) as file:
            i = 0
            for line in file:  # can be refactored with list comprehension
                l = []
                for j, ch in enumerate(line[:-1]):
                    pos = Position(i, j)
                    if ch == 'H':
                        l.append(Hero(pos))
                    elif ch == '$':
                        l.append(Monster(
                            pos,
                            Direction.UP,
                            random.choice([True, False])))
                    else:
                        is_passable = ch in self.PASSABLE
                        l.append(Cell(pos, is_passable, ch))
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
        return self.field[position.y][position.x]

    def __setitem__(self, position, value):
        self.field[position.y][position.x] = value

    def neighbours(self, cell):
        neighbours = []
        neighbours.append(self.field[cell.y - 1][cell.x])
        neighbours.append(self.field[cell.y][cell.x + 1])
        neighbours.append(self.field[cell.y + 1][cell.x])
        neighbours.append(self.field[cell.y][cell.x - 1])

        return neighbours

    def dist_between(self, cell1, cell2):
        return abs(cell1.y - cell2.y) + abs((cell1.x - cell2.x))

    def swap_cells(self, c1, c2):
        """ Swaps the position on the map of the passed cells """
        self[c1.position] = c2
        self[c2.position] = c1

        swap = c1.position
        c1.position = c2.position
        c2.position = swap

    def renew(self):
        self.__load_map()
