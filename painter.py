import pygame


class Painter(object):

  def demo(self):
    pygame.init()
    pygame.display.set_caption('Mario Clone')
    screen = pygame.display.set_mode((640, 480))

    clock = pygame.time.Clock()

    running = True
    px = pygame.PixelArray(screen)
    x = 0.0
    y = 0
    while running:
      dt = clock.tick(60)
      for a in range(128):
        px[int(x), y] = pygame.Color(255, 255, 255)
        x += 1
        if x >= 640:
          x = 0.0
          y += 1

      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
