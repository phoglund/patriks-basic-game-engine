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

import math
import pygame
import random

import arrays
import world


FALL_SPEED = 5
DOWN_LEFT = pygame.math.Vector2(-FALL_SPEED, FALL_SPEED)
DOWN_RIGHT = pygame.math.Vector2(FALL_SPEED, FALL_SPEED)
WHITE = pygame.Color(255, 255, 255)


class Snowfall(world.Drawable):

  _snowflake_progress = 0.5
  _progress_delta = 0.01
  _speed = DOWN_LEFT

  def __init__(self):
    # Each snowflake has two floats, one for x and one for y.
    self._snowflakes = arrays.FastPosArray()
    self._snow_piles = []

  @property
  def snowflakes(self):
    return self._snowflakes

  @property
  def snow_piles(self):
    return self._snow_piles

  def draw(self, screen, viewpoint_pos):
    for x, y in self._snowflakes.positions:
      screen.set_at((int(x - viewpoint_pos.x),
                     int(y - viewpoint_pos.y)), WHITE)

    for pile in self._snow_piles:
      pile.draw(screen, viewpoint_pos)

  def spawn_snowflakes(self):
    Snowfall.tick_snowflake_angle()
    for _ in range(10):
      self._snowflakes.append(x=200 + random.random() * 1000, y=0)

  def move_snow(self, obstacles, time_fraction):
    to_delete = []
    delta = Snowfall._speed * time_fraction
    for i in range(self._snowflakes.num_positions()):
      x, y = self._snowflakes.write_add(i, x=delta.x, y=delta.y)
      merged_with_snowpile = self._handle_snowpile_collisions(
          x, y, time_fraction)
      if merged_with_snowpile:
        to_delete.append(i)
      else:
        collided = self._handle_obstacle_collisions(
            obstacles, x, y, time_fraction)
        if collided:
          to_delete.append(i)

    # Sweep all the resting snowflakes we marked above.
    for index in sorted(to_delete, reverse=True):
      self._snowflakes.delete(index)

  def _handle_snowpile_collisions(self, x, y, time_fraction):
    for pile in self._snow_piles:
      if pile.bounding_rect.collidepoint(x, y):
        pile.add(snowflake_pos=pygame.math.Vector2(x, y))
        return True

    return False

  def _handle_obstacle_collisions(self, obstacles, x, y, time_fraction):
    for obstacle in obstacles:
      if not obstacle.bounding_rect.collidepoint(x, y):
        continue

      # Back up the snowflake until not colliding.
      pos = pygame.math.Vector2(x, y)
      while obstacle.bounding_rect.collidepoint(pos):
        pos -= Snowfall._speed * time_fraction * 0.1

      hit_top_of_obstacle = pos.y < obstacle.bounding_rect.top
      if not hit_top_of_obstacle:
        # Just ignore side hits on obstacles.
        return True

      # Landed on obstacle: spawn a snowpile on it.
      new_snowpile = spawn_snowpile(pos, spawned_on=obstacle)
      self._snow_piles.append(new_snowpile)
      return True

    # Did not collide with anything.
    return False

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


def spawn_snowpile(snowflake_pos: pygame.math.Vector2, spawned_on: world.Thing):
  ground_rect = spawned_on.bounding_rect

  # Limit the width for very large obstacles (like the ground) but don't go wider
  # than the obstacle we landed on.
  width = min(ground_rect.width, 200)
  num_columns = math.ceil(width / WIDTH_PER_COLUMN)

  # Spawn centered on the snowflake, but don't go off the edge of the obstacle.
  # Be forgiving if the snowflake isn't quite where it's supposed to be, i.e.
  # right on top of the obstacle (weird things happen when we back up for
  # collision).
  bottom_left = pygame.math.Vector2(
      snowflake_pos.x - width / 2, ground_rect.top + 1)
  if bottom_left.x < ground_rect.left:
    bottom_left.x = ground_rect.left
  if bottom_left.x + width > ground_rect.right:
    bottom_left.x = ground_rect.right - width

  return Snowpile(num_columns, bottom_left)


class Snowpile(world.Thing):

  def __init__(self, num_columns, bottom_left_pos: pygame.math.Vector2):
    self._snow_heights = [0] * num_columns
    self._bottom_left_pos = bottom_left_pos
    self._draw_bounding_box = False

  def add(self, snowflake_pos):
    # TODO: evaluate add algorithms. For now, just put the new flake in
    # a random location in the pile.
    # relative_pos = snowflake.at - self._bottom_left_pos
    # column = int(relative_pos.x / WIDTH_PER_COLUMN)
    # if column < 0 or column >= len(self._snow_heights):
      # This can happen if snowflakes hit from an angle.
    column = random.randint(0, len(self._snow_heights) - 1)

    self._snow_heights[column] += 1

  @property
  def bounding_rect(self):
    highest_column = max(self._snow_heights)
    if highest_column < FALL_SPEED * 2:
      # Make the bounding rect big enough to catch some snowflakes.
      highest_column = FALL_SPEED * 2
    top_left = self._bottom_left_pos - (0, highest_column)
    return pygame.Rect(top_left.x, top_left.y, WIDTH_PER_COLUMN *
                       len(self._snow_heights), highest_column)

  @property
  def has_custom_collision(self):
    return False

  def apply_custom_collision(self, player, current_speed):
    pass

  def draw(self, screen, viewpoint_pos):
    start = self._bottom_left_pos - viewpoint_pos
    end = pygame.math.Vector2(
        start.x + WIDTH_PER_COLUMN * len(self._snow_heights), start.y)

    def point_for_column(i, height):
      x = start.x + i * WIDTH_PER_COLUMN
      y = start.y - height
      return (x, y)

    midpoints = [point_for_column(i, height)
                 for i, height in enumerate(self._snow_heights)]
    pointlist = [start] + midpoints + [end]
    pygame.draw.polygon(screen, WHITE, pointlist)

    if self._draw_bounding_box:
      draw_rect = pygame.Rect(self.bounding_rect)
      draw_rect.topleft = draw_rect.topleft - viewpoint_pos
      pygame.draw.rect(screen, pygame.Color(255, 0, 0), draw_rect, 1)
