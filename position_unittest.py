import unittest

import position


class PositionTest(unittest.TestCase):

  def test_iterate_returns_x_then_y(self):
    p = position.make(1, 3)
    i = iter(p)
    self.assertEqual(1, next(i))
    self.assertEqual(3, next(i))
    with self.assertRaises(StopIteration):
      next(i)

  def test_getitem_returns_x_for_0(self):
    p = position.make(13, 14)
    self.assertEqual(13, p[0])

  def test_getitem_returns_y_for_1(self):
    p = position.make(13, 14)
    self.assertEqual(14, p[1])

  def test_adding_x(self):
    p = position.make(1, 3)
    p[0] += 2
    x, y = p
    self.assertEqual((3, 3), (x, y))

  def test_adding_position(self):
    p = position.make(1, 3)
    p += position.make(10, 10)
    self.assertEqual(p, position.make(11, 13))

if __name__ == '__main__':
  unittest.main()
