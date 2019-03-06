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
import pygame.freetype
import time

import world


PADDING = 5
SPACING = 10
RESIZE_AT_MOST_EVERY_X_SECS = 5


class DebugPanel(world.Drawable):

  def __init__(self, initial_position: pygame.math.Vector2):
    self._bounding_rect = pygame.Rect(
        initial_position.x, initial_position.y, 200, 100)
    self._debugged_values = {}
    self._font = pygame.freetype.SysFont('Courier New', 18)
    self._row_height = self._font.get_rect('A').height
    self._last_resize_time = 0

  @property
  def bounding_rect(self):
    return self._bounding_rect

  @property
  def debugged_values(self):
    return self._debugged_values

  @debugged_values.setter
  def debugged_values(self, new_values):
    new_values = {k: str(v) for k, v in new_values.items()}
    self._debugged_values = new_values

    # Resize to fit the new text (but not too often).
    if time.time() - self._last_resize_time < RESIZE_AT_MOST_EVERY_X_SECS:
      return

    self._last_resize_time = time.time()

    def rect_around_longest_value(values):
      longest_text = max(values, key=lambda k: len(k))
      return self._font.get_rect(longest_text)

    key_column = rect_around_longest_value(new_values.keys())
    value_column = rect_around_longest_value(new_values.values())

    self._bounding_rect.width = key_column.width + \
        value_column.width + PADDING * 2 + 40
    self._bounding_rect.height = (
        key_column.height + SPACING) * len(new_values.values())

  def draw(self, screen, viewpoint_pos):
    pygame.draw.rect(screen, pygame.Color(255, 0, 0), self._bounding_rect, 1)

    i = 0
    for key, value in self._debugged_values.items():
      x = self._bounding_rect.x + PADDING
      y = self._bounding_rect.y + PADDING + (SPACING + self._row_height) * i
      text = '%s: %s' % (key, value)
      self._font.render_to(screen, (x, y), text)
      i += 1


class NullDebugPanel(world.Drawable):

  def draw(self, screen, viewpoint_pos):
    pass
