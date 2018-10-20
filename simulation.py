import pygame
import random

import obstacles


class Simulation(object):

  def __init__(self, screen, size):
    self._screen = screen
    self._size = size
    self._viewpoint_pos = [0.0, 0.0]
    self._player_pos = [0.0, size[1] - 35]
    self._obstacles = [obstacles.random_obstacle(size)
                       for _ in range(20)]

  def advance(self, time_fraction):
    self._move_player(time_fraction)
    self._move_viewpoint(time_fraction)
    self._draw_player()
    self._draw_ground()
    self._draw_obstacles()

  def _move_player(self, time_fraction):
    speed = self._player_speed()

    self._player_pos[0] += speed * time_fraction

  def _move_viewpoint(self, time_fraction):
    # Just center on player for now.
    self._viewpoint_pos[0] = self._player_pos[0] - self._size[0] / 2

  def _draw_player(self):
    size = 20

    # Interpret _player_pos as the center of the player's body.
    x, y = self._player_pos
    x -= self._viewpoint_pos[0]

    rect = pygame.Rect(x - size / 2, y - size / 2, size, size)
    color = pygame.Color(255, 0, 128)
    pygame.draw.rect(self._screen, color, rect)
    head_pos = (int(x), int(y - size))
    pygame.draw.circle(self._screen, color, head_pos, 10)

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

  def _draw_ground(self):
    ground_color = pygame.Color(255, 128, 255)
    x_end, y_end = self._size
    ground_y = y_end - 20
    pygame.draw.line(self._screen, ground_color,
                     (0, ground_y), (x_end, ground_y), 5)

  def _draw_obstacles(self):
    viewpoint_x = int(self._viewpoint_pos[0])
    for obstacle in self._obstacles:
      obstacle.draw_to(self._screen, viewpoint_x)
