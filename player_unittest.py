import pygame
import unittest
from unittest import mock

import player


class PlayerTest(unittest.TestCase):

  def test_player_doesnt_move_if_no_keys_pressed(self):
    p = player.Player(start_pos=pygame.math.Vector2(14, 14))

    p.move(time_fraction=1.0)

    self.assertEqual((14, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_left_if_keyleft_pressed(self, get_pressed):
    get_pressed


# Initialize pygame once.
pygame.init()

if __name__ == '__main__':
  unittest.main()
