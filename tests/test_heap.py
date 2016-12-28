import unittest
from core.heap import Heap


class TestHeap(unittest.TestCase):
    def test(self):
        h = Heap()
        h.push(5)
        h.push(3)
        h.push(19)
        h.push(1)
        self.assertEqual(len(h), 4)
        self.assertTrue(19 in h)
        self.assertEqual(1, h.pop())
        self.assertEqual(3, h.pop())
        self.assertEqual(5, h.pop())
        self.assertEqual(19, h.pop())
        self.assertTrue(h.empty())
