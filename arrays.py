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

import array


# Impl note: Make this one a proper collections.abc.Sequence subclass if it
# gets longer than ~80 lines. This is fine for now.
class FastPosArray(object):
  """A fancy array that stores sets of 2 floats next to each other.

  The idea here is improve cache locality by putting 'positions'
  (i.e. coordinates of things) close to each other, since these
  positions are commonly updated together."""

  def __init__(self):
    self._positions = array.array('f')

  @property
  def all_positions(self):
    return ((self._positions[i], self._positions[i + 1])
            for i in range(0, len(self._positions), 2))

  def num_positions(self):
    return int(len(self._positions) / 2)

  def append(self, x, y):
    self._positions.append(x)
    self._positions.append(y)

  def write_add(self, index, x, y):
    self._positions[index * 2] += x
    self._positions[index * 2 + 1] += y
    return self._positions[index * 2: index * 2 + 2]

  def delete(self, index):
    del self._positions[index * 2: index * 2 + 2]
