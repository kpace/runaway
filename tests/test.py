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
        self.assertRaises(IndexError, map.__getitem__, (map.height-1 , map.width))
        self.assertRaises(IndexError, map.__getitem__, (100, 100))

    def test_setitem(self):
        map = Map('../maps/test-map1.txt')
        cell = Cell(symbol='!')
        map[(0, 0)] = cell
        map[(map.height - 1, map.width -1)] = cell
        self.assertEqual(map[0, 0], cell)
        self.assertEqual(map[(map.height - 1, map.width -1)], cell)

if __name__ == '__main__':
    unittest.main()
