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
  weather_god = world_controls.WeatherGod(game.snowfall)

  while True:
    screen.fill(COLOR_BLACK)
    dt = clock.tick(TARGET_FPS)
    game.advance(dt / TARGET_FPS)
    weather_god.act_on_input(game.viewpoint_pos)
    game.draw()
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.ACTIVEEVENT and event.state == 2:
        if event.gain:
          game.resume()
        else:
          game.suspend()
