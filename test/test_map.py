import unittest
from core.map import Map
from core.cells import Cell, Position


class TestMap(unittest.TestCase):
    def test_getitem(self):
        map = Map('maps/test-map1.txt')
        self.assertEqual(map[Position(0, 0)].symbol, '#')
        self.assertEqual(map[Position(1, 1)].symbol, ' ')
        self.assertEqual(map[Position(6, 3)].symbol, 'H')

    def test_getitem_bad_index(self):
        map = Map('maps/test-map1.txt')
        self.assertRaises(
                IndexError,
                map.__getitem__,
                Position(map.height, map.width - 1))
        self.assertRaises(
                IndexError,
                map.__getitem__,
                Position(map.height-1, map.width))
        self.assertRaises(
                IndexError,
                map.__getitem__,
                Position(100, 100))

    def test_setitem(self):
        map = Map('maps/test-map1.txt')
        cell = Cell(0, 0, symbol='!')
        map[Position(0, 0)] = cell
        map[Position(map.height - 1, map.width - 1)] = cell
        self.assertEqual(map[Position(0, 0)], cell)
        self.assertEqual(map[Position(map.height - 1, map.width - 1)], cell)

    def test_neighbours(self):
        map = Map('maps/test-map1.txt')
        neighbours = map.neighbours(map[Position(1, 2)])
        self.assertEqual(neighbours[0], map[Position(0, 2)])
        self.assertEqual(neighbours[1], map[Position(1, 3)])
        self.assertEqual(neighbours[2], map[Position(2, 2)])
        self.assertEqual(neighbours[3], map[Position(1, 1)])

    def test_dist_between(self):
        map = Map('maps/test-map1.txt')
        self.assertEqual(1, map.dist_between(
            map[Position(0, 0)], map[Position(0, 1)]))
        self.assertEqual(15, map.dist_between(
            map[Position(0, 0)], map[Position(5, 10)]))
        self.assertEqual(15, map.dist_between(
            map[Position(5, 10)], map[Position(0, 0)]))
        self.assertEqual(14, map.dist_between(
            map[Position(1, 0)], map[Position(5, 10)]))

    def test_swap_cells(self):
        map = Map('maps/test-map1.txt')
        c1 = map[Position(6, 2)]
        c2 = map[Position(6, 3)]
        map.swap_cells(c1, c2)
        self.assertEqual(c1, map[Position(6, 3)])
        self.assertEqual(c2, map[Position(6, 2)])
