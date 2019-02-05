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

import world


class Trampoline(world.Thing):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color

  def draw(self, screen, viewpoint_pos):
    draw_pos = self._rect.move(-viewpoint_pos)
    pygame.draw.rect(screen, self._color, draw_pos)

    # Draw a line through the top left corner.
    half_length = 10
    point_1 = pygame.math.Vector2(
        self._rect.topleft) + (half_length, -half_length) - viewpoint_pos
    point_2 = pygame.math.Vector2(
        self._rect.topleft) - (half_length, -half_length) - viewpoint_pos
    pygame.draw.line(screen, self._color, point_1, point_2)

  @property
  def bounding_rect(self):
    return self._rect

  @property
  def has_custom_collision(self):
    return True

  def apply_custom_collision(self, player, current_speed):
    player.launch_into_air(pygame.math.Vector2(
        current_speed.x * 10, -current_speed.y * 10))
    player.say('AAAAAAAAAAAAAAAAH!!!', duration_secs=2)


def random_trampoline(ground_y, bounds):
  x_end, _ = bounds
  x = random.randint(0, x_end)
  pos = pygame.Rect(x, ground_y - 10, 20, 20)
  color = pygame.Color(255, 0, 0)

  return Trampoline(pos, color)
