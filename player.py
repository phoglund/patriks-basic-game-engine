import pygame


class Player(object):

  def __init__(self, start_pos):
    self._position = start_pos

  @property
  def position(self):
    return self._position

  def move(self, time_fraction):
    speed = self._player_speed()

    self._position[0] += speed * time_fraction

  def draw(self, screen, viewpoint_pos):
    size = 20

    # Interpret _position as the center of the player's body.
    x, y = self._position
    viewpoint_x, _ = viewpoint_pos
    x -= viewpoint_x

    rect = pygame.Rect(x - size / 2, y - size / 2, size, size)
    color = pygame.Color(255, 0, 128)
    pygame.draw.rect(screen, color, rect)
    head_pos = (int(x), int(y - size))
    pygame.draw.circle(screen, color, head_pos, 10)

  def _player_speed(self):
    pressed = pygame.key.get_pressed()
    moving_left = pressed[pygame.K_LEFT]
    moving_right = pressed[pygame.K_RIGHT]
    if moving_left and moving_right:
      # Don't move in this case.
      return 0
    elif moving_left:
      return -5
    elif moving_right:
      return 5
    else:
      return 0
