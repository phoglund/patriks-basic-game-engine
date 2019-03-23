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
import time


class WeatherGod(object):

  def __init__(self, world_snowfall):
    self._snowfall = world_snowfall
    self._next_change_allowed_at = 0

  def act_on_input(self, viewpoint_pos):
    if time.time() < self._next_change_allowed_at:
      return

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_o]:
      self._snowfall.spawn_rate = max(self._snowfall.spawn_rate - 1, 0)
      self._rate_limit(max_changes_per_second=10)
    if pressed[pygame.K_p]:
      self._snowfall.spawn_rate = self._snowfall.spawn_rate + 1
      self._rate_limit(max_changes_per_second=10)

    button1, _, _ = pygame.mouse.get_pressed()
    if button1:
      clicked_at = pygame.mouse.get_pos()
      world_coords = pygame.math.Vector2(clicked_at) + viewpoint_pos
      self._snowfall.spawn_snowball(world_coords)
      self._rate_limit(max_changes_per_second=2)

  def _rate_limit(self, max_changes_per_second):
    self._next_change_allowed_at = time.time() + 1.0 / max_changes_per_second
