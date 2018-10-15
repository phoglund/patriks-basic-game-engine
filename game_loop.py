import pygame

import simulation


def demo():
  size = (640, 480)
  screen = pygame.display.set_mode(size)
  clock = pygame.time.Clock()

  game = simulation.Simulation(screen, size)

  running = True
  while running:
    dt = clock.tick(30)
    game.advance(dt / 30.0)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
