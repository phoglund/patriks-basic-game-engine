# Copyright 2019 Google LLC
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

import os
import unittest

import resources


# Mostly here to protect from resources.py moving.
class ResourcesTest(unittest.TestCase):

  def testFindsASound(self):
    file_that_should_exist = 'wind.wav'
    result = resources.sound_path(file_that_should_exist)
    self.assertTrue(os.path.exists(result),
                    msg='wind.wav should be in sounds/.')

  def testFindsAnImage(self):
    file_that_should_exist = 'snow.jpg'
    result = resources.image_path(file_that_should_exist)
    self.assertTrue(os.path.exists(result),
                    msg='snow.jpg should be in images/.')


if __name__ == '__main__':
  unittest.main()
