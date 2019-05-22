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
import pygame.freetype

import game_over
import simulation
import world_controls


TARGET_FPS = 30.0
COLOR_BLACK = pygame.Color(0, 0, 0)


def demo(start_hidden):
  size = (640, 480)
  screen = pygame.display.set_mode(size)
  if start_hidden:
    pygame.display.iconify()

  pygame.freetype.init()
  clock = pygame.time.Clock()
  game = simulation.Simulation(screen, pygame.math.Vector2(size), clock)
  weather_control = world_controls.WeatherControl(game.snowfall)
  world_editor = world_controls.WorldEditor(game)
  you_died = game_over.GameOverText()

  time_left = 0.0
  while True:
    screen.fill(COLOR_BLACK)
    dt = clock.tick(TARGET_FPS)
    time_left += dt / TARGET_FPS
    while time_left > 1.0:
      # TODO: apply alpha factor to all speed vectors at high FPS to fix jank.
      # https://www.gamedev.net/forums/topic/629618-proper-framerate-independent-game-loop/
      game.advance()
      time_left -= 1.0
    game.draw()
    if game.game_ended:
      you_died.draw(screen, game.viewpoint_pos)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.ACTIVEEVENT and event.state == 2:
        if event.gain:
          game.resume()
        else:
          game.suspend()

      if not world_editor.act_on_input(event, game.viewpoint_pos):
        weather_control.act_on_input(event, game.viewpoint_pos)
