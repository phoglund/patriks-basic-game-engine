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
    return None

  # There are two dimensions: x and y. Switch between them for the different layers of the tree
  # to get a good partitioning.
  axis = depth % 2
  sorted_list = sorted(obstacles, key=_sort_by_axis(axis))
  median = len(obstacles) // 2

  return _Node(sorted_list[median], 
               obstacle_kd_tree(sorted_list[:median], depth + 1), 
               obstacle_kd_tree(sorted_list[median + 1:], depth + 1))


def walk_topleft_bfs(node):
  def _walk(node):
    if not node:
      return ()
    topleft = node.obstacle.bounding_rect.topleft
    return (topleft, _walk(node.left), _walk(node.right))
  
  return _walk(node)


class _Node(collections.namedtuple('Node', 'obstacle left right')):
  def __repr__(self):
    return pprint.pformat(tuple(self))