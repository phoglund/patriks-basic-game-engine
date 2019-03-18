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

import cProfile
import pstats
import pygame
import tempfile

import simulation

pygame.init()
pygame.display.set_caption('Profiling mode...')
size = (640, 480)
screen = pygame.display.set_mode(size)
pygame.freetype.init()
clock = pygame.time.Clock()
game = simulation.Simulation(screen, pygame.math.Vector2(size), clock)


def advance_n_steps(n):
  for _ in range(n):
    game.advance(1.0)

with tempfile.NamedTemporaryFile() as stats_file:
  cProfile.run('advance_n_steps(100)', stats_file.name)
  stats = pstats.Stats(stats_file.name)
  stats.sort_stats('cumulative').print_stats(10)
