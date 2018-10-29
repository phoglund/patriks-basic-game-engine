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


class Box(object):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color

  def draw(self, screen, viewpoint_pos):
    viewpoint_pos_x, _ = viewpoint_pos
    translated = self._rect.move(-viewpoint_pos_x, 0)
    pygame.draw.rect(screen, self._color, translated, 1)

  @property
  def bounding_rect(self):
    return self._rect


class Ground(object):

  def __init__(self, y, initial_viewpoint_pos):
    self._y = y
    self._color = pygame.Color(255, 128, 128)
    self._viewpoint_pos = initial_viewpoint_pos
    self._width = 1000

  def draw(self, screen, viewpoint_pos):
    self._viewpoint_pos = viewpoint_pos
    self._width, _ = screen.get_size()
    pygame.draw.line(screen, self._color, (0, self._y),
                     (self._width, self._y), 5)

  @property
  def bounding_rect(self):
    # Move the bounding rect with the viewpoint - the ground is infinite.
    return pygame.Rect(self._viewpoint_pos.x, self._y, self._width, 30)


def random_obstacle(bounds):
  x_end, y_end = bounds
  size = 40 + int(random.uniform(-1.0, 1.0) * 20)
  x = random.randint(0, x_end)
  y = random.randint(0, y_end - size)

  rect = pygame.Rect(x, y, size, size)
  grayscale = random.randint(0, 255)
  color = pygame.Color(grayscale, grayscale, grayscale)

  return Box(rect, color)
