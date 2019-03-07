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


DOWN_LEFT = pygame.math.Vector2(-5, 5)
DOWN_RIGHT = pygame.math.Vector2(5, 5)
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

  def collides_with_snowpile(self, snow_pile, time_fraction):
    if not snow_pile.bounding_rect.collidepoint(self.at):
      return False

    self._resting = True
    return True

  def collision_adjust(self, obstacle, time_fraction):
    if not obstacle.bounding_rect.collidepoint(self.at):
      return False

    # Back up until not colliding with the obstacle.
    while obstacle.bounding_rect.collidepoint(self.at):
      self._position -= Snowflake._speed * time_fraction * 0.1

    self._resting = True
    return True

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


# Snow piles are represented like this:
#
# 1 2 1 0 1 2 3 ...
#             _
#   _       _/ \
#  / \_   _/    \
# /    \_/       \
#
# It's just bunch of heights. If a new snowflake lands, it increases
# the height of the nearest column somewhat.

# Total snowpile width = WIDTH_PER_COLUMN * num columns.
WIDTH_PER_COLUMN = 5


class Snowpile(world.Thing):

  def __init__(self, bottom_left_pos: pygame.math.Vector2):
    self._snow_heights = [0] * 20   # Always 20 for now.
    self._bottom_left_pos = bottom_left_pos

  def add(self, snowflake):
    relative_pos = snowflake.at - self._bottom_left_pos
    column = int(relative_pos.x / WIDTH_PER_COLUMN)
    if column < 0 or column >= len(self._snow_heights):
      print('Err, snowflake outside pile?')
      column = 0

    self._snow_heights[column] += 1

  @property
  def bounding_rect(self):
    highest_column = max(self._snow_heights)
    if highest_column < 10:
      highest_column = 10
    top_left = self._bottom_left_pos - (0, highest_column)
    return pygame.Rect(top_left.x, top_left.y, WIDTH_PER_COLUMN * len(self._snow_heights), highest_column)

  @property
  def has_custom_collision(self):
    return False

  def apply_custom_collision(self, player, current_speed):
    pass

  def draw(self, screen, viewpoint_pos):
    start = self._bottom_left_pos - viewpoint_pos

    def point_for_column(i, height):
      x = start.x + i * WIDTH_PER_COLUMN
      y = start.y - height
      return (x, y)

    def end_point():
      x = start.x + WIDTH_PER_COLUMN * len(self._snow_heights)
      y = start.y
      return (x, y)

    pointlist = [point_for_column(i, height)
                 for i, height in enumerate(self._snow_heights)]
    pointlist += [end_point()]
    pygame.draw.polygon(screen, WHITE, pointlist)
