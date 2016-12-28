import unittest
from core.cells import  Position


class TestPosition(unittest.TestCase):
    def test_eq(self):
        p1 = Position(5, 2)
        p2 = Position(5, 2)
        self.assertEqual(p1, p2)

    def test_add(self):
        p1 = Position(3, 1)
        p2 = Position(7, 11)
        p3 = p1 + p2
        self.assertEqual(p3.y, 10)
        self.assertEqual(p3.x, 12)

    def test_sub(self):
        p1 = Position(11, 2)
        p2 = Position(4, 1)
        p3 = p1 - p2
        self.assertEqual(p3, Position(7, 1))

if __name__ == '__main__':
    unittest.main()