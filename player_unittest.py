import pygame
import unittest
from unittest import mock

import player


def keys(pressed_keycodes):
  # pygame.key.get_pressed returns a bool list where
  # pressed[pygame.K_WHATEVER] == True means is the
  # key is pressed.
  return [x in pressed_keycodes for x in range(512)]


def make_player(start_pos):
  return player.Player(start_pos=pygame.math.Vector2(start_pos))


class PlayerTest(unittest.TestCase):

  def test_player_doesnt_move_if_no_keys_pressed(self):
    p = make_player(start_pos=(14, 14))

    p.move(time_fraction=1.0)

    self.assertEqual((14, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_left_if_keyleft_pressed(self, get_pressed):

    get_pressed.return_value = keys((pygame.K_LEFT,))
    p = make_player(start_pos=(14, 14))

    p.move(time_fraction=1.0)

    self.assertEqual((9, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_right_if_keyright_pressed(self, get_pressed):

    get_pressed.return_value = keys((pygame.K_RIGHT,))
    p = make_player(start_pos=(0, 0))

    p.move(time_fraction=1.0)
    p.move(time_fraction=1.0)

    self.assertEqual((10, 0), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_stays_still_if_both_left_right_pressed(self, get_pressed):

    get_pressed.return_value = keys((pygame.K_RIGHT, pygame.K_LEFT))
    p = make_player(start_pos=(0, 0))

    p.move(time_fraction=1.0)

    self.assertEqual((0, 0), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_scaled_to_time(self, get_pressed):

    get_pressed.return_value = keys((pygame.K_RIGHT,))
    p = make_player(start_pos=(0, 0))

    p.move(time_fraction=0.5)

    self.assertEqual((2.5, 0), p.at)


# Initialize pygame once.
pygame.init()

if __name__ == '__main__':
  unittest.main()
