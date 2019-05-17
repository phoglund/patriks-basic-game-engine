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

import functools
import os
import pygame
import random

import resources
import snow
import world


class Box(world.Thing):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color
    self._snowpile = snow.spawn_snowpile(spawned_on=rect)

  def draw(self, screen, viewpoint_pos):
    draw_pos = self._rect.move(-viewpoint_pos)
    pygame.draw.rect(screen, self._color, draw_pos, 0)
    self._snowpile.draw(screen, viewpoint_pos)

  @property
  def snowpile(self):
    return self._snowpile

  @property
  def bounding_rect(self):
    return self._rect

  @property
  def bounding_rect_with_snow(self):
    return self._rect.union(self._snowpile.bounding_rect)


class Ground(world.Thing):

  def __init__(self, y, initial_viewpoint_pos):
    # The ground is infinite forwards on the x axis for now.
    self._color = pygame.Color(255, 128, 128)
    self._pos = pygame.math.Vector2(-10000, y)
    self._image = None
    self._viewpoint_pos = initial_viewpoint_pos
    self._width = 1000
    # TODO: the ground snowpile doesn't work great if the ground is infinite.
    self._snowpile = snow.spawn_snowpile(pygame.Rect(0, y, 5000, 1))
    # Don't try to spawn snowflakes off the ground snowpile.
    self._snowpile.emit_snowflakes = False

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
    self._snowpile.draw(screen, viewpoint_pos)

  @property
  def bounding_rect(self):
    # Make the ground be very thick and basically infinite in both directions.
    return pygame.Rect(-10000000, self._pos.y, 200000000, 10000)

  @property
  def bounding_rect_with_snow(self):
    return self.bounding_rect.union(self._snowpile.bounding_rect)

  @property
  def snowpile(self):
    return self._snowpile


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
  ground = Ground(y, initial_viewpoint_pos)
  ground.load(resources.image_path('snow.jpg'))
  return ground
