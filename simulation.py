import pygame
import random

import player
import obstacles


def _generate_level(size, viewpoint_pos):
  some_obstacles = [obstacles.random_obstacle(size) for _ in range(20)]
  ground_level = size.y - 20
  ground = obstacles.Ground(
      y=ground_level, initial_viewpoint_pos=viewpoint_pos)
  return [ground] + some_obstacles


class Simulation(object):

  def __init__(self, screen, size: pygame.math.Vector2):
    self._screen = screen
    self._size = size
    self._viewpoint_pos = pygame.math.Vector2(0.0, 0.0)
    self._obstacles = _generate_level(size, self._viewpoint_pos)
    start_pos = pygame.math.Vector2(0.0, size.y - 100)
    self._player = player.Player(start_pos=start_pos)

  def advance(self, time_fraction):
    self._player.move(time_fraction)
    for obstacle in self._obstacles:
      self._player.collision_adjust(obstacle)
    self._move_viewpoint(self._player.at)
    self._player.draw(self._screen, self._viewpoint_pos)
    for obstacle in self._obstacles:
      obstacle.draw(self._screen, self._viewpoint_pos)

  def _move_viewpoint(self, player_pos):
    # Just center on player for now.
    self._viewpoint_pos.x = player_pos.x - self._size.x / 2
