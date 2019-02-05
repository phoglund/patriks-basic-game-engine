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
import pygame.freetype
import time


class SpeechBubble(object):

  def __init__(self, what_to_say, duration):
    self._what_to_say = what_to_say
    self._end_time = time.time() + duration
    self._font = pygame.freetype.SysFont('Comic Sans', 10)

  def draw(self, screen, x, y, player_head_radius):
    color = pygame.Color(128, 128, 0)
    text_bounds = self._font.get_rect(self._what_to_say)

    center = pygame.math.Vector2(
        x + text_bounds.width / 2, y - text_bounds.width / 2)
    padding = 5
    pygame.draw.circle(screen, color, (int(center.x),
                                       int(center.y)), int(text_bounds.width / 2) + padding)

    just_off_players_head = (x + player_head_radius + 5,
                             y - player_head_radius)
    center_left = (center.x - 10, center.y)
    center_right = (center.x + 10, center.y)
    pygame.draw.polygon(
        screen, color, [just_off_players_head, center_left, center_right])

    circle_left_edge = (center.x - text_bounds.width / 2, center.y)
    self._font.render_to(screen, circle_left_edge, self._what_to_say)

  def done(self):
    return time.time() > self._end_time


class NullSpeechBubble(object):

  def draw(self, screen, x, y, player_head_radius):
    pass

  def done(self):
    return False
