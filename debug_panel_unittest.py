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

import debug_panel


def _make_panel():
  return debug_panel.DebugPanel(pygame.math.Vector2(0, 0))


class DebugPanelTest(unittest.TestCase):

  def testResizesOnChangedValues(self):
    panel = _make_panel()
    width, height = (panel.bounding_rect.width, panel.bounding_rect.height)

    panel.debugged_values = {'key': 'val'}
    self.assertNotEqual(panel.bounding_rect.width, width)
    self.assertNotEqual(panel.bounding_rect.height, height)

  def testResizesToFitLongestKeyAndValue(self):
    panel = _make_panel()
    panel.debugged_values = {'looooooooooooooooooong key': 'val',
                             'key': 'loooooooooooooooong value'}
    width = panel.bounding_rect.width

    panel.debugged_values = {'looooooooooooooooooong key': 'slightly longer val',
                             'slightly longer key': 'loooooooooooooooong value'}

    self.assertEqual(panel.bounding_rect.width, width,
                     msg=('the shorter vals and keys were made a bit longer, '
                          'but that should not matter since they are still shorter.'))


if __name__ == '__main__':
  pygame.freetype.init()
  unittest.main()
