# Copyright 2018 Google LLC
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

# This is a very simple approximation of gravity: instead of modeling
# acceleration, we just interpolate the player delta-y to go down over
# time.
GRAVITY = pygame.math.Vector2(0, 20)


class Jump(object):
  """Contains the state of an ongoing jump."""

  def __init__(self, initial_speed):
    self._current_speed = initial_speed
    self._progress = 0.0

  def update(self):
    self._progress += 0.005
    if self._progress > 1.0:
      self._progress = 1.0

    self._current_speed = self._current_speed.lerp(GRAVITY, self._progress)

  @property
  def y(self):
    return self._current_speed.y


class NullJump(object):

  def update(self):
    pass

  @property
  def y(self):
    return GRAVITY.y
