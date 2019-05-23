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


def _to_world_coords(click_pos, viewpoint_pos):
  return pygame.math.Vector2(click_pos) + viewpoint_pos


class WeatherControl(object):

  def __init__(self, world_snowfall):
    self._snowfall = world_snowfall
    self._next_change_allowed_at = time.time()

  def act_on_input(self, pygame_event, viewpoint_pos):
    if time.time() < self._next_change_allowed_at:
      return

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_o]:
      self._snowfall.spawn_rate = max(self._snowfall.spawn_rate - 1, 0)
      self._rate_limit(max_changes_per_second=10)
    if pressed[pygame.K_p]:
      self._snowfall.spawn_rate = self._snowfall.spawn_rate + 1
      self._rate_limit(max_changes_per_second=10)

    if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
      world_coords = _to_world_coords(pygame_event.pos, viewpoint_pos)
      self._snowfall.spawn_snowball(world_coords)
      self._rate_limit(max_changes_per_second=2)

  def _rate_limit(self, max_changes_per_second):
    self._next_change_allowed_at = time.time() + 1.0 / max_changes_per_second


class WorldEditor(object):

  def __init__(self, simulation):
    self._simulation = simulation
    self._pointer_offset = None
    self._dragged_obstacle = None

  def act_on_input(self, pygame_event, viewpoint_pos):
    """Returns True if the event was consumed."""
    if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
      world_coords = _to_world_coords(pygame_event.pos, viewpoint_pos)
      obstacle = self._simulation.find_obstacle(at_position=world_coords)
      if not obstacle:
        return False

      rect = obstacle.bounding_rect
      self._pointer_offset = pygame.math.Vector2(
          rect.x - world_coords.x, rect.y - world_coords.y)
      self._dragged_obstacle = obstacle
      return True

    if pygame_event.type == pygame.MOUSEBUTTONUP and pygame_event.button == 1:
      self._dragged_obstacle = None
      self._pointer_offset = None
      self._simulation.after_obstacle_moved()
      return True

    if pygame_event.type == pygame.MOUSEMOTION:
      if self._dragged_obstacle:
        world_coords = _to_world_coords(pygame_event.pos, viewpoint_pos)
        new_pos = world_coords + self._pointer_offset
        old_rect = self._dragged_obstacle.bounding_rect
        new_rect = old_rect.copy()
        new_rect.x = new_pos.x
        new_rect.y = new_pos.y
        self._dragged_obstacle.move_or_resize(new_rect)
        return True

    return False
