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

import debug_panel
import obstacles
import player
import snow
import trampolines
import winds


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
    self.viewpoint_pos = pygame.math.Vector2(0.0, 0.0)
    self._obstacles = _generate_level(size, self.viewpoint_pos)
    start_pos = pygame.math.Vector2(size.x / 2, size.y - 100)
    self._player = player.Player(start_pos=start_pos)
    self._snowfall = snow.Snowfall()
    self._wind = winds.Gust(direction=pygame.math.Vector2(-1, 0))
    self._debug_panel = debug_panel.DebugPanel(pygame.math.Vector2(0, 0))

  @property
  def snowfall(self):
    return self._snowfall

  def advance(self, time_fraction):
    self._wind.update()
    self._player.move(time_fraction, self._wind)
    for obstacle in self._obstacles:
      # TODO(phoglund): Handle collisions uniformly with snow when it comes to
      # passing time_fraction.
      self._player.collision_adjust(obstacle)

    self._snowfall.spawn_snowflakes()
    self._snowfall.move_snow(self._obstacles, time_fraction, self._wind)
    self._move_viewpoint(self._player.at)

  def draw(self):
    self._player.draw(self._screen, self.viewpoint_pos)
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self.viewpoint_pos)

    self._snowfall.draw(self._screen, self.viewpoint_pos)

    self._debug_panel.debugged_values = {'flakes': self._snowfall.snowflakes.num_positions(),
                                         'fps': '%.1f' % self._master_clock.get_fps(),
                                         'spawn_rate': '%d' % self._snowfall.spawn_rate}
    self._debug_panel.draw(self._screen, self.viewpoint_pos)

  def _move_viewpoint(self, player_pos):
    # Just center on player for now, but clamp so we don't show too
    # much underground. Also don't move left of 0 since there's a
    # a bug with ground rendering I can't be bothered to fix.
    self.viewpoint_pos = player_pos - self._size / 2
    if self.viewpoint_pos.y > self._size.y * 0.1:
      self.viewpoint_pos.y = self._size.y * 0.1
    if self.viewpoint_pos.x < 0:
      self.viewpoint_pos.x = 0
