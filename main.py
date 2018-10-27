

import pygame
import sys

import game_loop


def main():
  pygame.init()
  pygame.display.set_caption('Mario Clone')

  game_loop.demo()

if __name__ == '__main__':
  sys.exit(main())
