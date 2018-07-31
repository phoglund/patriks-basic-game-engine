import pygame


class Painter(object):

  def demo(self):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    px = pygame.PixelArray(screen)
    for x in range(128):
      px[x, x] = pygame.Color(255, 255, 255)

    pygame.display.flip()

    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
