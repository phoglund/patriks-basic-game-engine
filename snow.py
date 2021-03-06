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

import functools
import math
import pygame
import random
import time

import arrays
import kdtree
import world
import winds


FALL_SPEED = 5
DOWN_LEFT = pygame.math.Vector2(-FALL_SPEED, FALL_SPEED)
DOWN_RIGHT = pygame.math.Vector2(FALL_SPEED, FALL_SPEED)
WHITE = pygame.Color(255, 255, 255)


class Snowfall(world.Drawable):

  _snowflake_progress = 0.5
  _progress_delta = 0.01
  speed = DOWN_LEFT

  def __init__(self):
    self._snowflakes = arrays.FastPosArray()
    self.spawn_rate = 40

  @property
  def snowflakes(self):
    return self._snowflakes

  def draw(self, screen, viewpoint_pos):
    for x, y in self._snowflakes.all_positions:
      screen.set_at((int(x - viewpoint_pos.x),
                     int(y - viewpoint_pos.y)), WHITE)

  def spawn_snowflakes(self):
    Snowfall.tick_snowflake_angle()
    for _ in range(self.spawn_rate):
      self._snowflakes.append(x=200 + random.random() * 1000, y=0)

  def spawn_snowball(self, position):
    # This is a pretty stupid algorithm but let's go with it for now.
    x_center = int(position.x)
    y_center = int(position.y)
    for x in range(x_center - 20, x_center + 20):
      for y in range(y_center - 20, y_center + 20):
        self._snowflakes.append(x=x, y=y)

  def move_snow(self, obstacles: kdtree.ObstacleKdTree, wind):
    to_delete = []
    delta = (Snowfall.speed + wind.windspeed)
    for i in range(self._snowflakes.num_positions()):
      x, y = self._snowflakes.write_add(i, x=delta.x, y=delta.y)
      collided = self._handle_snowflake_collision(obstacles, x, y)
      if collided:
        to_delete.append(i)

    # Sweep all the resting snowflakes we marked above. Go backwards
    # so we don't invalidate earlier indices.
    for index in sorted(to_delete, reverse=True):
      self._snowflakes.delete(index)

    for obstacle in obstacles.walk_preorder():
      drift_snow = obstacle.snowpile.drift_from_wind(wind)
      for flake in drift_snow:
        self._snowflakes.append(x=flake.x, y=flake.y)

  def _handle_snowflake_collision(self, obstacles, x, y):
    candidates = obstacles.quick_search(pos=(x, y))
    for obstacle in candidates:
      rect = obstacle.bounding_rect_with_snow
      if not rect.collidepoint(x, y):
        continue

      drift_snow = obstacle.snowpile.add(
          snowflake_pos=pygame.math.Vector2(x, y))
      for flake in drift_snow:
        self._snowflakes.append(x=flake.x, y=flake.y)
      return True

    # Did not collide with anything.
    return False

  @classmethod
  def tick_snowflake_angle(cls):
    cls._snowflake_progress += cls._progress_delta
    if cls._snowflake_progress >= 1.0:
      cls._snowflake_progress = 1.0
      cls._progress_delta = -0.02
    if cls._snowflake_progress <= 0.0:
      cls._snowflake_progress = 0.0
      cls._progress_delta = 0.02

    cls.speed = DOWN_LEFT.lerp(DOWN_RIGHT, cls._snowflake_progress)


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
WIDTH_PER_COLUMN = 2


def spawn_snowpile(spawned_on: pygame.Rect):
  num_columns = math.ceil(spawned_on.width / WIDTH_PER_COLUMN)
  return Snowpile(num_columns, pygame.math.Vector2(spawned_on.topleft))


def move_snowpile(snowpile, spawned_on: pygame.Rect):
  # TODO: does not deal with the spawned_on rect changing size.
  snowpile.move(pygame.math.Vector2(spawned_on.topleft))


class Snowpile(world.Thing):

  def __init__(self, num_columns, bottom_left_pos: pygame.math.Vector2):
    self._snow_heights = [0] * num_columns
    self._bottom_left_pos = bottom_left_pos
    self._draw_bounding_box = True
    self._estimated_height = 10
    self._next_bounds_update = time.time()
    self.emit_snowflakes = True

  def move(self, new_bottom_left_pos):
    self._bottom_left_pos = new_bottom_left_pos

  def add(self, snowflake_pos):
    relative_pos = snowflake_pos - self._bottom_left_pos
    column = int(relative_pos.x / WIDTH_PER_COLUMN)
    off_sides = column < 0 or column >= len(self._snow_heights)
    if off_sides or snowflake_pos.y > self._bottom_left_pos.y:
      # This can happen if snowflakes hit from an angle.
      column = random.randint(0, len(self._snow_heights) - 1)

    self._snow_heights[column] += 1
    self._maybe_estimate_height()

    return self._rebalance_snowpile(around_column=column)

  # TODO: unify with rebalancing, implement right drifting
  def drift_from_wind(self, wind):
    if not self.emit_snowflakes:
      # TODO: drifting looks weird on the ground, figure out what to do here.
      return []

    # Stronger wind = affect more of the snowpile.
    size = len(self._snow_heights)
    force_percentage = wind.windspeed.length() / winds.MAX_POSSIBLE_MAGNITUDE
    k = random.randint(0, int(size * force_percentage))
    columns = random.sample(range(size), k)

    left_wind = wind.windspeed.x < 0
    dislodged_flakes = int(10 * force_percentage)
    to_emit = 0
    if left_wind:
      for column in columns:
        self._snow_heights[column] -= dislodged_flakes
        to_emit += dislodged_flakes
        if self._snow_heights[column] < 0:
          to_emit -= self._snow_heights[column]
          self._snow_heights[column] = 0
      self._snow_heights[0] += to_emit
      return self._bleed_snowflakes_off_side(0, spawn_x=-5)
    else:
      pass

    return []

  def _rebalance_snowpile(self, around_column):
    left_side = around_column < len(self._snow_heights) / 2
    if left_side:
      return self._drift_snow_left(around_column)
    else:
      return self._drift_snow_right(around_column)

  def _drift_snow_left(self, column):
    def spawn_left():
      return self._bleed_snowflakes_off_side(0, spawn_x=-5)
    if column == 0:
      return spawn_left()

    # TODO: revisit this, why give up if diff < 3?
    diff = self._snow_heights[column] - self._snow_heights[column - 1]
    if diff < 3:
      return []
    drift_count = random.randint(1, int(diff / 2))

    self._snow_heights[column] -= drift_count

    while column >= 0:
      diff = self._snow_heights[column] - self._snow_heights[column - 1]
      if diff > drift_count:
        self._snow_heights[column - 1] += drift_count
        return []
      column -= 1

    self._snow_heights[0] += drift_count
    return spawn_left()

  def _drift_snow_right(self, column):
    rightmost = len(self._snow_heights) - 1

    def spawn_right():
      return self._bleed_snowflakes_off_side(rightmost, spawn_x=self.bounding_rect.width + 5)
    if column == rightmost:
      return spawn_right()

    diff = self._snow_heights[column] - self._snow_heights[column + 1]
    if diff < 3:
      return []
    drift_count = random.randint(1, int(diff / 2))

    self._snow_heights[column] -= drift_count

    rightmost = len(self._snow_heights) - 1
    while column < rightmost:
      diff = self._snow_heights[column] - self._snow_heights[column + 1]
      if diff > drift_count:
        self._snow_heights[column + 1] += drift_count
        return []
      column += 1

    self._snow_heights[rightmost] += drift_count
    return spawn_right()

  def _bleed_snowflakes_off_side(self, column, spawn_x):
    if self._snow_heights[column] < 3:
      return []

    spawn_count = self._snow_heights[column] - 3
    self._snow_heights[column] -= spawn_count
    if not self.emit_snowflakes:
      # Not emitting, just make 'em disappear.
      return []

    topleft = pygame.math.Vector2(self.bounding_rect.topleft)

    y_off_side = lambda: random.randint(0, self.bounding_rect.height)
    return [topleft + pygame.math.Vector2(spawn_x, y_off_side())
            for _ in range(spawn_count)]

  @functools.lru_cache()
  # Implementation note: bottom_left needs to be a parameter, or
  # the rect doesn't move when the obstacle moves.
  def _make_rect(self, height, bottom_left_pos_x, bottom_left_pos_y):
    if height < FALL_SPEED * 2:
      # Make the bounding rect big enough to catch some snowflakes.
      height = FALL_SPEED * 2
    top_left = self._bottom_left_pos - (0, height)
    return pygame.Rect(top_left.x, top_left.y, WIDTH_PER_COLUMN *
                       len(self._snow_heights), height)

  def _maybe_estimate_height(self):
    if time.time() < self._next_bounds_update:
      return

    self._estimated_height = sum(
        self._snow_heights) / len(self._snow_heights)
    self._next_bounds_update = time.time() + 5

  @property
  def bounding_rect(self):
    return self._make_rect(self._estimated_height, self._bottom_left_pos.x, self._bottom_left_pos.y)

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
