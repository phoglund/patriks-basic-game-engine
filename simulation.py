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
    self._snowflakes = []
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
    self._player.draw(self._screen, self._viewpoint_pos)
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self._viewpoint_pos)

    for snowflake in self._snowflakes:
      snowflake.draw(self._screen, self._viewpoint_pos)
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

    self._snowflakes.extend(new_snowflakes)

  def _handle_snowpile_collisions(self, snowflake, time_fraction):
    for pile in self._snow_piles:
      collided = snowflake.collides_with_snowpile(pile, time_fraction)
      if collided:
        pile.add(snowflake)
        return True

    return False

  def _handle_obstacle_collisions(self, snowflake, time_fraction):
    for obstacle in self._obstacles:
      collided = snowflake.collision_adjust(obstacle, time_fraction)
      if collided:
        hit_top_of_obstacle = snowflake.at.y < obstacle.bounding_rect.top
        if not hit_top_of_obstacle:
          # Just ignore side hits on obstacles.
          return

        # Landed on obstacle: spawn a snowpile on it.
        new_snowpile = snow.spawn_snowpile(
            snowflake.at, spawned_on=obstacle)
        self._snow_piles.append(new_snowpile)

  def _move_snow(self, time_fraction):
    for snowflake in self._snowflakes:
      snowflake.move(time_fraction)
      merged_with_snowpile = self._handle_snowpile_collisions(
          snowflake, time_fraction)
      if merged_with_snowpile:
        continue
      else:
        self._handle_obstacle_collisions(snowflake, time_fraction)

    # Sweep all the resting snowflakes we marked above. Flakes are marked as resting
    # if the collision algorithms above find collision.
    self._snowflakes[:] = [s for s in self._snowflakes if not s.resting]
