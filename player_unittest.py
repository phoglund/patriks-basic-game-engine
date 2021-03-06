# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygame
import unittest
from unittest import mock

import obstacles
import player
import winds


def move(player, wind=None):
  player.move(wind=wind or winds.NullWind())


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


def make_player_on_solid_ground(x=0, y=0):
  p = make_player((x, y))
  o = make_obstacle(x, p.bounding_rect.bottom)

  # First land on the obstacle; we can't jump in the air.
  p.collision_adjust(o)
  return o, p


class PlayerTest(unittest.TestCase):

  def test_player_doesnt_move_if_no_keys_pressed(self):
    o, p = make_player_on_solid_ground(14, 14)

    move(p)
    p.collision_adjust(o)

    self.assertEqual((14, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_left_if_keyleft_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_LEFT])
    o, p = make_player_on_solid_ground(14, 14)

    move(p)
    p.collision_adjust(o)

    self.assertEqual((9, 14), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_moves_right_if_keyright_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_RIGHT])
    o, p = make_player_on_solid_ground()

    move(p)
    p.collision_adjust(o)
    move(p)
    p.collision_adjust(o)

    self.assertEqual((10, 0), p.at)

  @mock.patch('pygame.key.get_pressed')
  def test_player_stays_still_if_both_left_right_pressed(self, get_pressed):

    get_pressed.return_value = keys([pygame.K_RIGHT, pygame.K_LEFT])
    o, p = make_player_on_solid_ground()

    move(p)
    p.collision_adjust(o)

    self.assertEqual((0, 0), p.at)

  def test_player_is_affected_by_wind(self):
    o, p = make_player_on_solid_ground()

    start_x = p.at.x
    move(p, wind=winds.StaticWind(windspeed=pygame.math.Vector2(-1, 0)))
    self.assertLess(p.at.x, start_x)

  def test_bounding_rect_centers_on_player_body(self):
    o, p = make_player_on_solid_ground()

    b = p.bounding_rect
    self.assertLess(b.topleft, (0, 0))
    self.assertGreater(b.bottomright, (0, 0))
    self.assertEqual(b.centerx, 0)
    self.assertEqual(b.centery, 0)

  @mock.patch('pygame.key.get_pressed')
  def test_bounding_rect_follows_player(self, get_pressed):
    get_pressed.return_value = keys([pygame.K_RIGHT])
    o, p = make_player_on_solid_ground()

    move(p)
    p.collision_adjust(o)

    b = p.bounding_rect

    self.assertEqual(b.centerx, p.at.x)
    self.assertEqual(b.centery, p.at.y)

  @mock.patch('pygame.key.get_pressed')
  def test_jumping_player_goes_up(self, get_pressed):
    o, p = make_player_on_solid_ground(0, 400)
    get_pressed.return_value = keys([pygame.K_SPACE])
    move(p)
    p.collision_adjust(o)
    y1 = p.at.y
    move(p)
    p.collision_adjust(o)
    y2 = p.at.y

    # Note that negative y = up.
    self.assertLessEqual(y1, 400)
    self.assertLess(y2, y1)

  @mock.patch('pygame.key.get_pressed')
  def test_jumping_player_eventually_comes_down(self, get_pressed):
    p = make_player((0, 0))
    o = make_obstacle(0, 0)

    get_pressed.return_value = keys([pygame.K_SPACE])
    move(p)
    p.collision_adjust(o)
    get_pressed.return_value = keys([])

    for _ in range(100):
      move(p)
      p.collision_adjust(o)

    self.assertEqual(p.at, (0, p.bounding_rect.y / 2))

  def test_collision_adjust_land_on_top_of_obstacle(self):
    # Spawn in the air slightly above the obstacle.
    p = make_player((0, 300))
    o = make_obstacle(0, 400)

    for _ in range(200):
      move(p)
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
    move(p)
    p.collision_adjust(o)

    self.assertAlmostEqual(p.bounding_rect.bottom, 418, delta=1)
    self.assertLess(p.at.x, 1)

# Initialize pygame once.
pygame.init()

if __name__ == '__main__':
  unittest.main()
