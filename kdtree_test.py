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

import pygame
import unittest

import kdtree


def obstacle(x, y, width=10, height=10):
  class FakeObstacle(object):

    def __init__(self, bounding_rect):
      self._bounding_rect = bounding_rect

    @property
    def bounding_rect(self):
      return self._bounding_rect

    def __repr__(self):
      return str(self._bounding_rect)

  rect = pygame.Rect(x, y, width, height)
  return FakeObstacle(rect)


class ObstacleKdTreeTest(unittest.TestCase):

  def test_walk_preorder_is_actually_preorder(self):
    # Pre-order traversal: root, left, right.
    #     (5, 6)
    #   (3, 4)   (7, 8)
    # (1, 2)
    obstacles = (obstacle(1, 2), obstacle(3, 4),
                 obstacle(5, 6), obstacle(7, 8))
    tree = kdtree.obstacle_kd_tree(obstacles, depth=0)
    result = list(tree.walk_preorder())
    self.assertEqual(len(result), 4)
    l1, l2, root, r = obstacles
    self.assertEqual(result[0], root)
    self.assertEqual(result[1], l2)
    self.assertEqual(result[2], l1)
    self.assertEqual(result[3], r)

  def test_insert_partitions_on_topleft(self):
    obstacles = (obstacle(100, 100), obstacle(50, 100), obstacle(200, 100))
    tree = kdtree.obstacle_kd_tree(obstacles, depth=0)
    result = [o.bounding_rect.topleft for o in tree.walk_preorder()]
    expected = [(100, 100), (50, 100), (200, 100)]
    self.assertEqual(result, expected,
                     msg=('depth=0, so we are splitting on x. Therefore '
                          '(100, 100) is the median; it should be root. '
                          '(50, 100) goes into the left subtree and '
                          '(200, 100) into the right subtree.'))

  def test_insert_switches_between_x_and_y_axis(self):
    obstacles = (obstacle(1, 20), obstacle(2, 19), obstacle(3, 18),
                 obstacle(4, 17), obstacle(5, 16), obstacle(6, 15))
    tree = kdtree.obstacle_kd_tree(obstacles)
    result = [o.bounding_rect.topleft for o in tree.walk_preorder()]
    # Sketch of the expected tree:
    #
    #               (4, 17)
    #    (2, 19)               (5, 16)
    # (3, 18)  (1, 20)    (6, 15)      None
    left = [(2, 19), ((3, 18)), (1, 20)]
    right = [(5, 16), (6, 15)]
    expected = [(4, 17)] + left + right
    self.assertEqual(result, expected,
                     msg=('See expected tree. Notably, (3, 18 is left of '
                          '(2, 19) because 18 < 19; at depth = 1 we are '
                          'looking at y and not x as in the level above.'))

  def test_search_culls_rects_left_and_above_1(self):
    obstacles = (obstacle(100, 100), obstacle(50, 100), obstacle(200, 100))
    tree = kdtree.obstacle_kd_tree(obstacles)
    hits = tree.search((0, 0))
    self.assertEqual(hits, ())

  def test_search_culls_rects_left_and_above_2(self):
    obstacles = (obstacle(100, 100), obstacle(50, 100), obstacle(200, 100))
    tree = kdtree.obstacle_kd_tree(obstacles)
    hits = tree.search((0, 101))
    result = [o.bounding_rect.topleft for o in hits]
    self.assertEqual(result, [(50, 100)])


if __name__ == '__main__':
  unittest.main()
