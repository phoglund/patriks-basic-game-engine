import math
import pygame

import jump


def to_draw_coords(pos, viewpoint_pos):
  # Draw depending on where the viewpoint is.
  x, y = (pos - viewpoint_pos)

  # Always round the same way to avoid skitting.
  return pygame.math.Vector2(math.floor(x), math.floor(y))


class Player(object):

  BODY_SIZE = 20
  HEAD_RADIUS = 10

  def __init__(self, start_pos: pygame.math.Vector2):
    self._position = start_pos
    self._speed = pygame.math.Vector2(0, 0)
    self._ground_y = start_pos.y  # TODO: proper ground collision detection.
    self._current_jump = jump.NullJump()
    self._draw_bounding_rect = True

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

  def move(self, time_fraction: float):
    self._speed = self._player_speed()

    self._position += self._speed * time_fraction
    if self._position.y > self._ground_y:
      # Don't let the player fall under the ground.
      self._position.y = self._ground_y
      self._current_jump = jump.NullJump()

  def collision_adjust(self, obstacle):
    them = obstacle.bounding_rect
    us = self.bounding_rect

    if not them.colliderect(us):
      return

    # Adjust back our position depending on which direction we were going in.
    def adjust_x():
      # if us.bottom >= them.top or us.top <= them.bottom:
      #   return False  # Above or below the obstacle, don't collide x
      if self._speed.x > 0:
        self._position.x = them.left - us.width / 2
        return True
      elif self._speed.x < 0:
        self._position.x = them.right + us.width / 2
        return True

    if adjust_x():
      return
    if self._speed.y > 0:
      print(them, us)
      us.bottom = them.top
      self._position.y = us.centery
    elif self._speed.y < 0:
      us.top = them.bottom
      self._position.y = us.centery

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

    jumping = pressed[pygame.K_SPACE]
    if jumping and self._current_jump.done():
      self._current_jump = jump.Jump(pygame.math.Vector2(x, -20))
    self._current_jump.update()
    y = self._current_jump.y

    return pygame.math.Vector2(x, y)
