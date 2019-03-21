# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import snow


class SnowTest(unittest.TestCase):

  def test_storing_position_in_array(self):
    array = snow.FastPosArray()
    array.append(1, 2)
    array.append(3, 4)
    array.append(5, 6)

    result = array.positions
    self.assertEqual(next(result), (1, 2))
    self.assertEqual(next(result), (3, 4))
    self.assertEqual(next(result), (5, 6))
    with self.assertRaises(StopIteration):
      next(result)

  def test_num_positions(self):
    array = snow.FastPosArray()
    array.append(1, 2)
    array.append(3, 4)

    self.assertEqual(array.num_positions(), 2)

  def test_writing_adding_to_array(self):
    array = snow.FastPosArray()
    array.append(1, 2)
    array.append(3, 4)

    x1, y1 = array.write_add(0, 1, 1)
    x2, y2 = array.write_add(1, 1, 1)
    stored = array.positions
    self.assertEqual((x1, y1), (2, 3))
    self.assertEqual(next(stored), (2, 3))
    self.assertEqual((x2, y2), (4, 5))
    self.assertEqual(next(stored), (4, 5))

  def test_deleting_one(self):
    array = snow.FastPosArray()
    array.append(16, 17)
    array.append(18, 19)

    array.delete(1)
    result = array.positions
    self.assertEqual(array.num_positions(), 1)
    self.assertEqual(next(result), (16, 17))
    with self.assertRaises(StopIteration):
      next(result)


if __name__ == '__main__':
  unittest.main()
