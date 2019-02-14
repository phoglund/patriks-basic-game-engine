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

import world


DOWN_LEFT = pygame.math.Vector2(-1, 1)
DOWN_RIGHT = pygame.math.Vector2(1, 1)
WHITE = pygame.Color(255, 255, 255)


class Snowflake(world.Drawable):

  _snowflake_progress = 0.0
  _progress_delta = 0.01
  _speed = DOWN_LEFT

  def __init__(self, position):
    self._position = position
    self._resting = False

  @property
  def at(self):
    return self._position

  @property
  def resting(self):
    return self._resting

  def draw(self, screen, viewpoint_pos):
    at = self._position - viewpoint_pos
    screen.set_at((int(at.x), int(at.y)), WHITE)

  def move(self, time_fraction):
    self._position += Snowflake._speed * time_fraction

  def collision_adjust(self, obstacle, time_fraction):
    if not obstacle.bounding_rect.collidepoint(self.at):
      return

    self._back_up_and_rest(time_fraction)

  def collision_adjust_resting_snowflake(self, other_snowflake, time_fraction):
    if other_snowflake.at != self.at:
      return

    self._back_up_and_rest(time_fraction)

  def _back_up_and_rest(self, time_fraction):
    self._position -= Snowflake._speed * time_fraction
    self._resting = True

  @classmethod
  def tick_snowflake_angle(cls):
    cls._snowflake_progress += cls._progress_delta
    if cls._snowflake_progress >= 1.0:
      cls._snowflake_progress = 1.0
      cls._progress_delta = -0.01
    if cls._snowflake_progress <= 0.0:
      cls._snowflake_progress = 0.0
      cls._progress_delta = 0.01

    cls._speed = DOWN_LEFT.lerp(DOWN_RIGHT, cls._snowflake_progress)
