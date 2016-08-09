import random

from core.cells import Hero, Monster
import sys
from core.heap import Heap


class GameManager:
    def __init__(self, map, initial_direction=(0, 1)):
        self.game_over = False
        self.map = map
        self.hero = self.get_hero()
        self.monsters = self.get_monsters()
        self.direction = initial_direction

    def move_cell(self, cell, to):
        if to.passable:
            self.map.swap_cells(cell, to)
            return True
        else:
            return False

    def move_hero(self):
        to_move_pos = tuple(map(sum, zip(self.hero.position, self.direction)))
        to_move_cell = self.map[to_move_pos]
        if self.move_cell(self.hero, to_move_cell):
            self.update_monsters_path()
            return True
        else:
            return False

    def move_monsters(self):
        for monster in self.monsters:
            to_move = None
            # monster.path could be empty, if a_star can't find path
            if monster.path and monster.chasing:
                to_move = monster.path.pop()
            else:
                to_move = self.map[tuple(map(sum, zip(monster.position, monster.direction)))]
                if not to_move.passable:
                    neighbours = list(filter(lambda c: c.passable, self.map.neighbours(monster)))
                    if neighbours:
                        to_move = random.choice(neighbours)
            if to_move:
                # TODO: implement Position class, it will be easier
                # TODO: to substract and add positions
                import operator
                monster.direction = tuple(map(operator.sub, to_move.position, monster.position))
                if to_move == self.hero:  # Game Over
                    self.game_over = True
                    return
                self.move_cell(monster, to_move)

    def update_monsters_path(self):
        """ Updates all monsters paths if hero position is changed.
            Note: a_star can return empty list, if path isn't found
        """
        for monster in self.monsters:
            monster.path = self.a_star(monster, self.hero)

    def get_hero(self):
        # TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return x

    def get_monsters(self):
        return [self.map[(i, j)] for i in range(self.map.height) for j in
                range(self.map.width) if type(self.map[(i, j)]) is Monster]

    def dimensions(self):
        return self.map.height, self.map.width

    def cell_at(self, position):
        return self.map[position]

    def a_star(self, start, goal):
        g_score = {
            start: 0
        }

        f_score = {
            start: g_score[start] + self.heuristic_cost(start, goal)
        }

        came_from = {}
        open = Heap(key=lambda x: f_score[x])
        closed = set()

        open.push(start)  # add start to open

        while not open.empty():
            current = open.pop()
            closed.add(current)

            if current is goal:
                return self.reconstruct_path(came_from, goal)

            for n in self.map.neighbours(current):
                # if current is not passable but is Monster
                # find path through it, because it will move in the future
                # TODO: Think about better implementation
                if (not n.passable and type(n) != Monster) or n in closed:
                    continue

                tentative = g_score[current] + self.map.dist_between(current, n)

                if n not in open \
                        or tentative < g_score.get(n, sys.maxsize):

                    came_from[n] = current
                    g_score[n] = tentative
                    f_score[n] = g_score[n] + self.heuristic_cost(n, goal)
                    if n not in open:
                        open.push(n)
        return []

    def heuristic_cost(self, start, goal):
        return self.map.dist_between(start, goal)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current:
            current = came_from.get(current, False)
            if current:
                path.append(current)
        return path[:len(path) - 1]

    def set_direction(self, direction):
        to_move_pos = tuple(map(sum, zip(self.hero.position, direction)))
        if self.map[to_move_pos].passable:
            self.direction = direction

    def toggle_chasing(self):
        for monster in self.monsters:
            monster.chasing = random.choice([True, False])