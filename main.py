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

import argparse
import pygame
import sys

import game_loop


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--start_hidden', action='store_true',
                      help='hide the game on start', required=False)
  return parser.parse_args()


def main():
  pygame.init()
  pygame.display.set_caption('Platform Game')

  args = parse_args()
  game_loop.demo(args.start_hidden)

if __name__ == '__main__':
  sys.exit(main())
