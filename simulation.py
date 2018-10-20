import pygame
import random

import player
import obstacles


class Simulation(object):

  def __init__(self, screen, size):
    self._screen = screen
    self._size = size
    self._viewpoint_pos = [0.0, 0.0]
    self._obstacles = [obstacles.random_obstacle(size)
                       for _ in range(20)]
    self._player = player.Player(start_pos=[0.0, size[1] - 35])

  def advance(self, time_fraction):
    self._player.move(time_fraction)
    self._move_viewpoint(self._player.position)
    self._player.draw(self._screen, self._viewpoint_pos)
    self._draw_ground()
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self._viewpoint_pos)

  def _move_viewpoint(self, player_pos):
    # Just center on player for now.
    self._viewpoint_pos[0] = player_pos[0] - self._size[0] / 2

  def _draw_ground(self):
    ground_color = pygame.Color(255, 128, 255)
    x_end, y_end = self._size
    ground_y = y_end - 20
    pygame.draw.line(self._screen, ground_color,
                     (0, ground_y), (x_end, ground_y), 5)
