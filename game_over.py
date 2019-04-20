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

import pygame

import world


TEXT_COLOR = pygame.Color(255, 255, 255)
BACKGROUND_COLOR = pygame.Color(0, 0, 0)


class GameOverText(world.Drawable):
  def __init__(self):
    self._font = pygame.freetype.SysFont('Arial', 40)
    self._line1 = "R.I.P 2019-2019"
    self._line2 = "REST IN PEPERONIS"

  def draw(self, screen, viewpoint_pos):
    width, height = screen.get_size()
    x = width / 6
    y = height / 2
    self._font.render_to(screen, (x, y), self._line1, fgcolor=TEXT_COLOR, bgcolor=BACKGROUND_COLOR)
    self._font.render_to(screen, (x, y + height / 6), self._line2, fgcolor=TEXT_COLOR, bgcolor=BACKGROUND_COLOR)

