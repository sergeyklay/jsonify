# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import current_app

from bot.app import create_app


class TestClass:
    def setup_method(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown_method(self) -> None:
        self.app_context.pop()

    def test_app_exist(self) -> None:
        assert current_app is not None

    def test_app_is_testing(self):
        assert current_app.config['TESTING']
