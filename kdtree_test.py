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
  
  rect = pygame.Rect(x, y, width, height)    
  return FakeObstacle(rect)


class ObstacleKdTreeTest(unittest.TestCase):
  def test_insert_partitions_on_topleft(self):
    obstacles = (obstacle(100, 100), obstacle(50, 100), obstacle(200, 100))
    tree = kdtree.obstacle_kd_tree(obstacles, depth=0)
    result = kdtree.walk_topleft_bfs(tree)
    expected = ((100, 100), ((50, 100), (), ()), ((200, 100), (), ()))
    self.assertEqual(result, expected, 
                     msg=('depth=0, so we are splitting on x. Therefore '
                          '(100, 100) is the median; it should be root. '
                          '(50, 100) goes into the left subtree and '
                          '(200, 100) into the right subtree.'))



if __name__ == '__main__':
  unittest.main()
