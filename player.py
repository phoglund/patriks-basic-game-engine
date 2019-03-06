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

import math
import pygame

import jump
import speech_bubble
import world


def to_draw_coords(pos, viewpoint_pos):
  # Draw depending on where the viewpoint is.
  return pos - viewpoint_pos


class Player(world.Thing):

  BODY_SIZE = 20
  HEAD_RADIUS = 10

  def __init__(self, start_pos: pygame.math.Vector2):
    self._position = start_pos
    self._speed = pygame.math.Vector2(0, 0)
    self._current_jump = jump.NullJump()
    self._draw_bounding_rect = False
    self._on_solid_ground = False
    self._currently_saying = speech_bubble.NullSpeechBubble()

  @property
  def at(self) -> pygame.math.Vector2:
    return self._position

  @property
  def bounding_rect(self):
    # See draw(). The player is a rect with a circle on top.
    width = Player.BODY_SIZE
    height = Player.BODY_SIZE + Player.HEAD_RADIUS * 2
    x, y = self._position
    return pygame.Rect(x - width / 2, y - height / 2, width, height)

  def move(self, time_fraction: float=1.0):
    self._speed = self._player_speed() * time_fraction

    self._position += self._speed

    if self._currently_saying.done():
      self._currently_saying = speech_bubble.NullSpeechBubble()

  def collision_adjust(self, obstacle):
    if not obstacle.bounding_rect.colliderect(self.bounding_rect):
      return

    if obstacle.has_custom_collision:
      obstacle.apply_custom_collision(player=self, current_speed=self._speed)
    else:
      # Otherwise: apply the normal algorithm.
      self._back_up_until_not_colliding(obstacle)

  def say(self, what_to_say, duration_secs=5):
    self._currently_saying = speech_bubble.SpeechBubble(
        what_to_say, duration_secs)

  def _back_up_until_not_colliding(self, obstacle):
    them = obstacle.bounding_rect

    # Reverse time until we no longer collide.
    fraction_undone = 0.0
    while them.colliderect(self.bounding_rect) and fraction_undone < 1.0:
      self._position -= self._speed * 0.1
      fraction_undone += 0.1

    # Then, try moving forward each axis as much as possible.
    # We can only hit a side or top of the rect at a time, so don't
    # block movement in the other direction (this means we can slide)
    # down the side of an obstacle and not get stuck in the side,
    # for instance.
    # TODO: probably causes the confusion below.
    self._position.x += self._speed.x
    if them.colliderect(self.bounding_rect):
      self._position.x -= self._speed.x
    self._position.y += self._speed.y
    if them.colliderect(self.bounding_rect):
      self._position.y -= self._speed.y
      self._on_solid_ground = True
      self._current_jump = jump.NullJump()
    else:
      self._on_solid_ground = False

    if fraction_undone >= 1.0:
      # TODO: this happens when colliding with several obstacles at once.
      # Find some way to deal with this.
      print("collision algorithm is confused", flush=True)

  def draw(self, screen, viewpoint_pos: pygame.math.Vector2):
    # Interpret _position as the center of the player's bounding rect.
    x, y = to_draw_coords(self._position, viewpoint_pos)

    body_size = Player.BODY_SIZE
    head_radius = Player.HEAD_RADIUS
    head_height = head_radius * 2
    body = pygame.Rect(
        x - body_size / 2, y - (body_size - head_height) / 2, body_size, body_size)
    color = pygame.Color(255, 0, 128)
    pygame.draw.rect(screen, color, body)
    head_pos = (int(x), int(y - head_height / 2))
    pygame.draw.circle(screen, color, head_pos, head_radius)

    if self._draw_bounding_rect:
      draw_rect = pygame.Rect(self.bounding_rect)
      draw_rect.topleft = to_draw_coords(draw_rect.topleft, viewpoint_pos)
      pygame.draw.rect(screen, pygame.Color(255, 0, 0), draw_rect, 1)

    self._currently_saying.draw(screen, x, y, head_radius)

  def _player_speed(self) -> pygame.Vector2:
    pressed = pygame.key.get_pressed()

    moving_left = pressed[pygame.K_LEFT]
    moving_right = pressed[pygame.K_RIGHT]

    x = 0
    if moving_left and moving_right:
      # Don't move in this case.
      x = 0
    elif moving_left:
      x = -5
    elif moving_right:
      x = 5

    wants_to_jump = pressed[pygame.K_SPACE]
    if wants_to_jump and self._on_solid_ground:
      self._current_jump = jump.Jump(pygame.math.Vector2(x, -20))
      self._on_solid_ground = False
    self._current_jump.update()
    y = self._current_jump.y

    return pygame.math.Vector2(x, y)

  def launch_into_air(self, direction):
    # Doesn't have to be into the air per se, but that's the most common case.
    self._current_jump = jump.Jump(direction)
