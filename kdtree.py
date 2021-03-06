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


import collections
import functools
import pprint
import pygame


def _sort_by_axis(axis):
  assert axis < 2, 'axis is either 0 = x, or 1 = y'

  def _key(item):
    topleft = item.bounding_rect.topleft
    return topleft[axis]

  return _key


# Heavily inspired by the example in https://en.wikipedia.org/wiki/K-d_tree.
def obstacle_kd_tree(obstacles, depth=0):
  if not obstacles:
    return NullKdTree()

  # There are two dimensions: x and y. Switch between them for the different layers of the tree
  # to get a good partitioning.
  axis = depth % 2
  sorted_list = sorted(obstacles, key=_sort_by_axis(axis))
  median = len(obstacles) // 2

  return ObstacleKdTree(sorted_list[median],
                        obstacle_kd_tree(sorted_list[:median], depth + 1),
                        obstacle_kd_tree(sorted_list[median + 1:], depth + 1))


class ObstacleKdTree(object):

  def __init__(self, obstacle, left, right):
    self.obstacle = obstacle
    self.left = left
    self.right = right

  def __repr__(self):
    return pprint.pformat(tuple(self))

  def search(self, pos):
    return self._search(pos, depth=0)

  def quick_search(self, pos):
    # Implementation note: quantize the position to improve the hit rate for
    # the memoizing lru cache. The returned results could miss some obstacles
    # if they're just outside the step, so use where we don't need 100%
    # precision.
    step = 20
    x, y = pos
    quantized_pos = (x // step * step, y // step * step)
    return self._memoized_search(quantized_pos)

  @functools.lru_cache(maxsize=2048)
  def _memoized_search(self, pos):
    return self._search(pos, depth=0)

  def _search(self, pos, depth):
    axis = depth % 2
    current = self.obstacle.bounding_rect.topleft

    if pos[axis] < current[axis]:
      return self.left._search(pos, depth + 1)
    else:
      return ((self.obstacle,) +
              self.left._search(pos, depth + 1) +
              self.right._search(pos, depth + 1))

  def walk_preorder(self):
    yield self.obstacle
    for obstacle in self.left.walk_preorder():
      yield obstacle
    for obstacle in self.right.walk_preorder():
      yield obstacle


class NullKdTree(ObstacleKdTree):

  def __init__(self):
    super().__init__(None, None, None)

  def _search(self, pos, depth):
    return ()

  def walk_preorder(self):
    return ()
