import pygame

import position
import simulation


TARGET_FPS = 30.0
COLOR_BLACK = pygame.Color(0, 0, 0)


def demo():
  size = position.make(640, 480)
  screen = pygame.display.set_mode(size)
  clock = pygame.time.Clock()

  game = simulation.Simulation(screen, size)

  running = True
  while running:
    screen.fill(COLOR_BLACK)
    dt = clock.tick(TARGET_FPS)
    game.advance(dt / TARGET_FPS)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
