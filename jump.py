import pygame

# This is a very simple approximation of gravity: instead of modeling
# acceleration, we just interpolate the player delta-y to go down over
# time.
GRAVITY = pygame.math.Vector2(0, 10)


class Jump(object):
  """Contains the state of an ongoing jump."""

  def __init__(self, initial_speed):
    self._current_speed = initial_speed
    self._progress = 0.0

  def update(self):
    self._progress += 0.01
    if self._progress > 1.0:
      self._progress = 1.0

    self._current_speed = self._current_speed.lerp(GRAVITY, self._progress)

  @property
  def y(self):
    return self._current_speed.y


class NullJump(object):

  def update(self):
    pass

  @property
  def y(self):
    return GRAVITY.y
