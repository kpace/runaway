import unittest
from core.map import Map
from core.cells import Cell


class TestMap(unittest.TestCase):
    def test_getitem(self):
        map = Map('../maps/test-map1.txt')
        self.assertEqual(map[(0, 0)].symbol, '#')
        self.assertEqual(map[(1, 1)].symbol, ' ')
        self.assertEqual(map[(6, 3)].symbol, 'H')

    def test_getitem_bad_index(self):
        map = Map('../maps/test-map1.txt')
        self.assertRaises(IndexError, map.__getitem__, (map.height, map.width - 1))
        self.assertRaises(IndexError, map.__getitem__, (map.height-1, map.width))
        self.assertRaises(IndexError, map.__getitem__, (100, 100))

    def test_setitem(self):
        map = Map('../maps/test-map1.txt')
        cell = Cell(0, 0, symbol='!')
        map[(0, 0)] = cell
        map[(map.height - 1, map.width -1)] = cell
        self.assertEqual(map[0, 0], cell)
        self.assertEqual(map[(map.height - 1, map.width -1)], cell)

    def test_neighbours(self):
        map = Map('../maps/test-map1.txt')
        neighbours = map.neighbours(map[(1, 2)])
        self.assertEqual(neighbours[0], map[2, 2])
        self.assertEqual(neighbours[1], map[0, 2])
        self.assertEqual(neighbours[2], map[1, 3])
        self.assertEqual(neighbours[3], map[1, 1])

    def test_dist_between(self):
        map = Map('../maps/test-map1.txt')
        self.assertEqual(1, map.dist_between(map[(0, 0)], map[0, 1]))
        self.assertEqual(15, map.dist_between(map[(0, 0)], map[5, 10]))
        self.assertEqual(15, map.dist_between(map[(5, 10)], map[0, 0]))
        self.assertEqual(14, map.dist_between(map[(1, 0)], map[5, 10]))


if __name__ == '__main__':
    unittest.main()
