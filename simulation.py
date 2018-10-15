import pygame
import random


class Obstacle(object):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color

  def draw_to(self, screen, viewpoint_pos_x):
    translated = self._rect.move(viewpoint_pos_x, 0)
    pygame.draw.rect(screen, self._color, translated)


def random_obstacle(bounds):
  x_end, y_end = bounds
  size = 40
  x = random.randint(0, x_end)
  y = random.randint(0, y_end - size)

  rect = pygame.Rect(x, y, size, size)
  grayscale = random.randint(0, 255)
  color = pygame.Color(grayscale, grayscale, grayscale)

  return Obstacle(rect, color)


class Simulation(object):

  def __init__(self, screen, size):
    self._screen = screen
    self._size = size
    self._viewpoint_pos_x = 0.0
    self._viewpoint_x_speed = 5.0
    self._obstacles = [random_obstacle(size) for _ in xrange(20)]

  def advance(self, fraction):
    self._viewpoint_pos_x += self._viewpoint_x_speed * fraction
    self._draw_ground()
    self._draw_obstacles(self._viewpoint_pos_x)

    pygame.display.flip()

  def _draw_ground(self):
    ground_color = pygame.Color(255, 128, 255)
    x_end, y_end = self._size
    ground_y = y_end - 20
    pygame.draw.line(self._screen, ground_color,
                     (0, ground_y), (x_end, ground_y), 5)

  def _draw_obstacles(self, viewpoint_pos_x):
    for obstacle in self._obstacles:
      obstacle.draw_to(self._screen, int(viewpoint_pos_x))
