import pygame
import random

import player
import obstacles


class Simulation(object):

  def __init__(self, screen, size: pygame.math.Vector2):
    self._screen = screen
    self._size = size
    self._viewpoint_pos = pygame.math.Vector2(0.0, 0.0)
    self._obstacles = [obstacles.random_obstacle(size)
                       for _ in range(20)]
    start_pos = pygame.math.Vector2(0.0, size.y - 35)
    self._player = player.Player(start_pos=start_pos)

  def advance(self, time_fraction):
    self._player.move(time_fraction)
    self._move_viewpoint(self._player.at)
    self._player.draw(self._screen, self._viewpoint_pos)
    self._draw_ground()
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self._viewpoint_pos)

  def _move_viewpoint(self, player_pos):
    # Just center on player for now.
    self._viewpoint_pos.x = player_pos.x - self._size.x / 2

  def _draw_ground(self):
    ground_color = pygame.Color(255, 128, 255)
    ground_y = self._size.y - 20
    pygame.draw.line(self._screen, ground_color,
                     (0, ground_y), (self._size.x, ground_y), 5)
