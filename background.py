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

import world


class Background(world.Drawable):

  def __init__(self):
    self._image = None

  def load(self, image_path):
    loaded_image = pygame.image.load(image_path)
    self._image = loaded_image.convert()

  def draw(self, screen, viewpoint_pos):
    assert self._image

    # Parallax scroll according to the viewpoint position.
    source_area = pygame.Rect(500 - viewpoint_pos.x / 2,
                              500 - viewpoint_pos.y / 2, 640, 480)
    screen.blit(self._image, -viewpoint_pos / 2, source_area)


def load_background():
  this_scripts_dir = os.path.realpath(os.path.dirname(__file__))

  background = Background()
  background.load(os.path.join(this_scripts_dir, 'images', 'mountains.jpg'))
  return background
