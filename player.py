import pygame


class Player(object):

  SIZE = 20

  def __init__(self, start_pos: pygame.math.Vector2):
    self._position = start_pos
    self._ground_y = start_pos.y  # TODO: proper ground collision detection.
    self._current_jump = NullJump()
    self._draw_bounding_rect = True

  @property
  def at(self) -> pygame.math.Vector2:
    return self._position

  @property
  def bounding_rect(self):
        # See draw(). The player is a rect with a circle on top.
    size = Player.SIZE
    head_size = 10
    x, y = self._position
    return pygame.Rect(x - size / 2, y - size - head_size,
                       size, size * 2 + head_size / 2)

  def move(self, time_fraction: float):
    speed = self._player_speed()

    self._position += speed * time_fraction
    if self._position.y > self._ground_y:
      # Don't let the player fall under the ground.
      self._position.y = self._ground_y
      self._current_jump = NullJump()

  def draw(self, screen, viewpoint_pos: pygame.math.Vector2):
    # Interpret _position as the center of the player's body.
    x, y = (self._position - viewpoint_pos)

    size = Player.SIZE
    rect = pygame.Rect(x - size / 2, y - size / 2, size, size)
    color = pygame.Color(255, 0, 128)
    pygame.draw.rect(screen, color, rect)
    head_pos = (int(x), int(y - size))
    pygame.draw.circle(screen, color, head_pos, 10)

    if self._draw_bounding_rect:
      pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                       self.bounding_rect.move(-viewpoint_pos), 1)

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
      self._current_jump = Jump(pygame.math.Vector2(x, -5))
    self._current_jump.update()
    y = self._current_jump.y

    return pygame.math.Vector2(x, y)


class Jump(object):
  """Contains the state of an ongoing jump."""

  # This is a very simple approximation of gravity: instead of modeling
  # acceleration, we just interpolate the player delta-y to go down over
  # time.
  GRAVITY = pygame.math.Vector2(0, 5)

  def __init__(self, initial_speed):
    self._current_speed = initial_speed
    self._progress = 0.0

  def done(self):
    return self._progress >= 1.0

  def update(self):
    self._progress += 0.01
    self._current_speed = self._current_speed.lerp(
        Jump.GRAVITY, self._progress)

  @property
  def y(self):
    return self._current_speed.y


class NullJump(object):

  def done(self):
    return True

  def update(self):
    pass

  @property
  def y(self):
    return 0
