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
import random
import time


class Wind(object):

  def __init__(self, windspeed: pygame.math.Vector2):
    self.windspeed = windspeed

  def update(self):
    pass


class Gust(Wind):

  def __init__(self, direction: pygame.math.Vector2):
    super().__init__(direction)
    self._initial_windspeed = direction
    self._next_change_allowed_at = time.time()

  def update(self):
    if time.time() < self._next_change_allowed_at:
      return

    self.windspeed = self._initial_windspeed * random.randint(0, 20)
    self._rate_limit(max_changes_per_second=1.0)

  def _rate_limit(self, max_changes_per_second):
    self._next_change_allowed_at = time.time() + 1.0 / max_changes_per_second


class NullWind(Wind):

  def __init__(self):
    super().__init__(windspeed=pygame.math.Vector2(0, 0))


class StaticWind(Wind):

  def __init__(self, windspeed):
    super().__init__(windspeed)
