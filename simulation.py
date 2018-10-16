import pygame
import random

import obstacles


class Simulation(object):

  def __init__(self, screen, size):
    self._screen = screen
    self._size = size
    self._viewpoint_pos_x = 0.0
    self._obstacles = [obstacles.random_obstacle(size)
                       for _ in xrange(20)]

  def advance(self, time_fraction):
    self._move_player(time_fraction)
    self._draw_ground()
    self._draw_obstacles(self._viewpoint_pos_x)

  def _move_player(self, time_fraction):
    speed = self._player_speed()

    self._viewpoint_pos_x += speed * time_fraction

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

  def _draw_obstacles(self, viewpoint_pos_x):
    for obstacle in self._obstacles:
      obstacle.draw_to(self._screen, int(viewpoint_pos_x))
