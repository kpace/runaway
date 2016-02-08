from cells import Hero, Monster
import sys
import heapq

class GameManager:
    def __init__(self, map):
        self.game_over = False
        self.map = map
        self.hero = self.get_hero()
        self.monster = self.get_monster()
        self.hero_position = self.get_hero_position()

    def move_cells(self, direction):
        if self.move_hero(direction):
            self.monster.path = self.a_star(self.monster, self.hero)

        to_move = self.monster.path.pop()
        if to_move == self.hero:
            self.game_over = True
        self.move_cell(self.monster, to_move)

    def move_cell(self, cell, to):
        if to.passable:
            self.map.swap_cells(cell, to)

    def move_hero(self, direction):
        to_move_pos = tuple(map(sum, zip(self.hero_position, direction)))
        to_move_cell = self.map[to_move_pos]

        if to_move_cell and to_move_cell.passable:
            self.map[to_move_pos] = self.hero
            to_move_cell.y, to_move_cell.x = self.hero_position
            self.map[self.hero_position] = to_move_cell
            self.hero_position = to_move_pos
            self.hero.y, self.hero.x = to_move_pos
            return True

        return False

    def get_hero(self):
        # TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return x

    def get_hero_position(self):
        # TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return i, j

    def get_monster(self):
        # TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Monster:
                    return x

    def dimensions(self):
        return self.map.height, self.map.width

    def symbol_at(self, position):
        return self.map[position].symbol

    def a_star(self, start, goal):
        g_score = {
            start: 0
        }

        f_score = {
            start: g_score[start] + self.heuristic_cost(start, goal)
        }

        came_from = {}
        open = []
        closed = set()

        heapq.heappush(open, (f_score[start], start))  # add start to open

        while open:
            _, current = heapq.heappop(open)
            closed.add(current)

            if current is goal:
                return self.reconstruct_path(came_from, goal)  # path has been found

            for n in self.map.neighbours(current):
                if not n.passable or n in closed:
                    continue

                tentative = g_score[current] + self.map.dist_between(current, n)

                if n not in open \
                        or tentative < g_score.get(n, sys.maxsize):

                    came_from[n] = current
                    g_score[n] = tentative
                    f_score[n] = g_score[n] + self.heuristic_cost(n, goal)
                    if n not in open:
                        heapq.heappush(open, (f_score[n], n))

    def heuristic_cost(self, start, goal):
        return self.map.dist_between(start, goal)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current:
            current = came_from.get(current, False)
            if current:
                path.append(current)
        return path[:len(path) - 1]
