from cells import Hero, Monster
import sys
import heapq

class GameManager:
    def __init__(self, map, initial_direction=(0, 1)):
        self.game_over = False
        self.map = map
        self.hero = self.get_hero()
        self.monsters = self.get_monsters()
        self.hero_position = self.get_hero_position()
        self.direction = initial_direction

    def move_cells(self):
        if self.move_hero():
            self.update_monsters_path()
        self.move_monsters()

    def move_cell(self, cell, to):
        if to.passable:
            self.map.swap_cells(cell, to)

    def move_hero(self):
        # TODO: implement get_next_cell
        to_move_pos = tuple(map(sum, zip(self.hero_position, self.direction)))
        to_move_cell = self.map[to_move_pos]

        # TODO: implement swap_cells
        if to_move_cell and to_move_cell.passable:
            self.map[to_move_pos] = self.hero
            to_move_cell.y, to_move_cell.x = self.hero_position
            self.map[self.hero_position] = to_move_cell
            self.hero_position = to_move_pos
            self.hero.y, self.hero.x = to_move_pos
            return True

        return False

    def move_monsters(self):
        for monster in self.monsters:
            # monster.path could be empty, if a_star can't find path
            if monster.path:
                to_move = monster.path.pop()
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

    def get_hero_position(self):
        # TODO: think about refactoring this
        for i in range(self.map.height):
            for j in range(self.map.width):
                x = self.map[(i, j)]
                if type(x) is Hero:
                    return i, j

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
        open = []
        closed = set()

        heapq.heappush(open, (f_score[start], start))  # add start to open

        while open:
            _, current = heapq.heappop(open)
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
                        heapq.heappush(open, (f_score[n], n))
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
        to_move_pos = tuple(map(sum, zip(self.hero_position, direction)))
        if self.map[to_move_pos].passable:
            self.direction = direction
