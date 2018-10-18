import pygame
import random


class Box(object):

  def __init__(self, rect, color):
    self._rect = rect
    self._color = color

  def draw_to(self, screen, viewpoint_pos_x):
    translated = self._rect.move(-viewpoint_pos_x, 0)
    pygame.draw.rect(screen, self._color, translated)


def random_obstacle(bounds):
  x_end, y_end = bounds
  size = 40 + int(random.uniform(-1.0, 1.0) * 20)
  x = random.randint(0, x_end)
  y = random.randint(0, y_end - size)

  rect = pygame.Rect(x, y, size, size)
  grayscale = random.randint(0, 255)
  color = pygame.Color(grayscale, grayscale, grayscale)

  return Box(rect, color)
