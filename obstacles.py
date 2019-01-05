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

import os
import pygame
import random

import world


class Box(world.Thing):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color

  def draw(self, screen, viewpoint_pos):
    draw_pos = self._rect.move(-viewpoint_pos)
    pygame.draw.rect(screen, self._color, draw_pos, 0)

  @property
  def bounding_rect(self):
    return self._rect


class Ground(world.Thing):

  def __init__(self, y, initial_viewpoint_pos):
    # The ground is infinite on the x axis for now.
    self._color = pygame.Color(255, 128, 128)
    self._pos = pygame.math.Vector2(-1000, y)
    self._image = None
    self._viewpoint_pos = initial_viewpoint_pos
    self._width = 1000

  def load(self, image_path):
    loaded_image = pygame.image.load(image_path)
    self._image = loaded_image.convert()

  def draw(self, screen, viewpoint_pos):
    assert self._image
    self._viewpoint_pos = viewpoint_pos
    self._width = screen.get_width()
    draw_pos = self._pos - viewpoint_pos
    viewpoint_width = screen.get_width()
    while draw_pos.x < viewpoint_pos.x + viewpoint_width:
      screen.blit(self._image, draw_pos)
      draw_pos.x += self._image.get_width()

  @property
  def bounding_rect(self):
    # Move the bounding rect with the viewpoint - the ground is infinite.
    very_high_height = 10000
    return pygame.Rect(self._viewpoint_pos.x, self._pos.y, self._width, very_high_height)


def random_obstacle(bounds):
  x_end, y_end = bounds
  size = 40 + int(random.uniform(-1.0, 1.0) * 20)
  x = random.randint(300, x_end)
  y = random.randint(0, y_end - size)

  rect = pygame.Rect(x, y, size, size)
  grayscale = random.randint(0, 255)
  color = pygame.Color(grayscale, grayscale, grayscale)

  return Box(rect, color)


def load_ground(y, initial_viewpoint_pos):
  this_scripts_dir = os.path.realpath(os.path.dirname(__file__))

  ground = Ground(y, initial_viewpoint_pos)
  ground.load(os.path.join(this_scripts_dir, 'images', 'snow.jpg'))
  return ground
