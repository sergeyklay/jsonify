# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import unittest

from flask import current_app

from app import create_app


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_app_exist(self) ->None:
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
