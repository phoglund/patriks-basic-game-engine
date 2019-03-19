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

import array
import pygame
import random

import background
import debug_panel
import obstacles
import player
import snow
import trampolines


def _generate_level(size, viewpoint_pos):
  some_obstacles = [obstacles.random_obstacle(size) for _ in range(20)]
  ground_level = size.y - 20
  ground = obstacles.load_ground(
      y=ground_level, initial_viewpoint_pos=viewpoint_pos)
  some_trampolines = [trampolines.random_trampoline(
      ground_y=ground_level, bounds=size) for _ in range(0)]
  return [ground] + some_obstacles + some_trampolines


class Simulation(object):

  def __init__(self, screen, size: pygame.math.Vector2, clock: pygame.time.Clock):
    self._screen = screen
    self._size = size
    self._master_clock = clock
    self._viewpoint_pos = pygame.math.Vector2(0.0, 0.0)
    self._obstacles = _generate_level(size, self._viewpoint_pos)
    start_pos = pygame.math.Vector2(size.x / 2, size.y - 100)
    self._player = player.Player(start_pos=start_pos)
    self._background = background.load_background()
    self._snowflakes = array.array('f')
    self._snow_piles = []
    self._debug_panel = debug_panel.DebugPanel(pygame.math.Vector2(0, 0))

  def advance(self, time_fraction):
    # self._background.draw(self._screen, self._viewpoint_pos)
    self._player.move(time_fraction)
    for obstacle in self._obstacles:
      # TODO(phoglund): Handle collisions uniformly with snow when it comes to
      # passing time_fraction.
      self._player.collision_adjust(obstacle)

    self._spawn_snowflakes()
    self._move_snow(time_fraction)
    self._move_viewpoint(self._player.at)

  def draw(self):
    self._player.draw(self._screen, self._viewpoint_pos)
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self._viewpoint_pos)

    for i in range(0, len(self._snowflakes), 2):
      x, y = self._snowflakes[i:i + 2]
      x -= self._viewpoint_pos.x
      y -= self._viewpoint_pos.y
      self._screen.set_at((int(x), int(y)), snow.WHITE)
    for pile in self._snow_piles:
      pile.draw(self._screen, self._viewpoint_pos)

    self._debug_panel.debugged_values = {'piles': len(self._snow_piles),
                                         'active': len(self._snowflakes),
                                         'fps': '%.1f' % self._master_clock.get_fps(),
                                         'player_y': '%.1f' % self._player.at.y}
    self._debug_panel.draw(self._screen, self._viewpoint_pos)

  def _move_viewpoint(self, player_pos):
    # Just center on player for now, but clamp so we don't show too
    # much underground. Also don't move left of 0 since there's a
    # a bug with ground rendering I can't be bothered to fix.
    self._viewpoint_pos = player_pos - self._size / 2
    if self._viewpoint_pos.y > self._size.y * 0.1:
      self._viewpoint_pos.y = self._size.y * 0.1
    if self._viewpoint_pos.x < 0:
      self._viewpoint_pos.x = 0

  def _spawn_snowflakes(self):
    snow.Snowflake.tick_snowflake_angle()
    new_snowflakes = [snow.Snowflake(
        pygame.math.Vector2(200 + random.random() * 1000, 0)
    ) for _ in range(10)]

    for _ in range(10):
      # TODO: this way of representing snowflakes is way faster but pretty
      # ugly. Find some way of maybe restoring the Snowflake abstraction
      # or at least make this look a bit nicer.
      x = 200 + random.random() * 1000
      y = 0
      self._snowflakes.append(x)
      self._snowflakes.append(y)

  def _handle_snowpile_collisions(self, x, y, time_fraction):
    for pile in self._snow_piles:
      if pile.bounding_rect.collidepoint(x, y):
        pile.add(snowflake_pos=pygame.math.Vector2(x, y))
        return True

    return False

  def _handle_obstacle_collisions(self, x, y, time_fraction):
    for obstacle in self._obstacles:
      if not obstacle.bounding_rect.collidepoint(x, y):
        continue

      # Back up the snowflake until not colliding.
      pos = pygame.math.Vector2(x, y)
      while obstacle.bounding_rect.collidepoint(pos):
        pos -= snow.Snowflake._speed * time_fraction * 0.1

      hit_top_of_obstacle = pos.y < obstacle.bounding_rect.top
      if not hit_top_of_obstacle:
        # Just ignore side hits on obstacles.
        return True

      # Landed on obstacle: spawn a snowpile on it.
      new_snowpile = snow.spawn_snowpile(pos, spawned_on=obstacle)
      self._snow_piles.append(new_snowpile)
      return True

    # Did not collide with anything.
    return False

  def _move_snow(self, time_fraction):
    to_delete = []
    for i in range(0, len(self._snowflakes), 2):
      self._snowflakes[i] += snow.Snowflake._speed.x * time_fraction
      self._snowflakes[i + 1] += snow.Snowflake._speed.y * time_fraction
      x, y = self._snowflakes[i:i + 2]
      merged_with_snowpile = self._handle_snowpile_collisions(
          x, y, time_fraction)
      if merged_with_snowpile:
        to_delete.append(i)
      else:
        collided = self._handle_obstacle_collisions(x, y, time_fraction)
        if collided:
          to_delete.append(i)

    # Sweep all the resting snowflakes we marked above.
    for index in sorted(to_delete, reverse=True):
      del self._snowflakes[index:index + 2]
