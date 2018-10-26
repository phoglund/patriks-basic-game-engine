import pygame
import unittest
from unittest import mock

import obstacles
import player


def keys(pressed_keycodes):
  # pygame.key.get_pressed returns a bool list where
  # pressed[pygame.K_WHATEVER] == True means is the
  # key is pressed.
  return [x in pressed_keycodes for x in range(512)]


def make_player(start_pos):
  return player.Player(start_pos=pygame.math.Vector2(start_pos))


def make_obstacle(x=0, y=0, width=20, height=20):
  color = pygame.Color(255, 255, 255)
  return obstacles.Box(pygame.Rect(x, y, width, height), color)


class PlayerTest(unittest.TestCase):

  def test_player_doesnt_move_if_no_keys_pressed(self):
    p = make_player((14, 14))

    p.move()

    self.assertEqual((14, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_left_if_keyleft_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_LEFT])
    p = make_player((14, 14))

    p.move()

    self.assertEqual((9, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_right_if_keyright_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_RIGHT])
    p = make_player((0, 0))

    p.move()
    p.move()

    self.assertEqual((10, 0), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_stays_still_if_both_left_right_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_RIGHT, pygame.K_LEFT])
    p = make_player((0, 0))

    p.move()

    self.assertEqual((0, 0), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_scaled_to_time(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_RIGHT])
    p = make_player((0, 0))

    p.move(time_fraction=0.5)

    self.assertEqual((2.5, 0), p.at)

  def test_bounding_rect_centers_on_player_body(self):
    p = make_player((0, 0))

    b = p.bounding_rect
    self.assertLess(b.topleft, (0, 0))
    self.assertGreater(b.bottomright, (0, 0))
    self.assertEqual(b.centerx, 0)
    # The head stands ~16 pixels above the body, but the bb
    # needs to cover the head too so it's a bit off center.
    self.assertEqual(b.centery, 0)

  @mock.patch('pygame.key.get_pressed')
  def test_bounding_rect_follows_player(self, get_pressed):
    get_pressed.return_value = keys([pygame.K_RIGHT])
    p = make_player((0, 0))

    p.move()

    b = p.bounding_rect

    self.assertEqual(b.centerx, p.at.x)
    self.assertEqual(b.centery, p.at.y)

  @mock.patch('pygame.key.get_pressed')
  def test_jumping_player_goes_up(self, get_pressed):
    p = make_player((0, 400))

    get_pressed.return_value = keys([pygame.K_SPACE])
    p.move()
    y1 = p.at.y
    p.move()
    y2 = p.at.y

    # Note that negative y = up.
    self.assertLess(y1, 400)
    self.assertLess(y2, y1)

  @mock.patch('pygame.key.get_pressed')
  def test_jumping_player_eventually_comes_down(self, get_pressed):
    p = make_player((0, 0))

    get_pressed.return_value = keys([pygame.K_SPACE])
    p.move()
    get_pressed.return_value = keys([])

    for _ in range(100):
      p.move()

    self.assertEqual(p.at, (0, 0))

  def test_collision_adjust_land_on_top_of_obstacle(self):
    # Spawn in the air slightly above the obstacle.
    # TODO: hack air spawn until proper ground collision implemented.
    p = make_player((0, 500))
    p._on_solid_ground = False
    p.at.y = 350
    o = make_obstacle(0, 400)

    for _ in range(200):
      p.move()
      p.collision_adjust(o)

    self.assertEqual(p.bounding_rect.bottom, 400,
                     msg='Should have landed on obstacle')
    self.assertEqual(p.at.x, 0)

  @mock.patch('pygame.key.get_pressed')
  def test_collision_adjust_move_on_obstacle(self, get_pressed):
    # Spawn on the obstacle.
    p = make_player((0, 400))
    o = make_obstacle(0, 400, 20)

    get_pressed.return_value = keys([pygame.K_LEFT])
    p.move()

    self.assertEqual(p.bounding_rect.bottom, 420)
    self.assertLess(p.at.x, 0)

# Initialize pygame once.
pygame.init()

if __name__ == '__main__':
  unittest.main()
