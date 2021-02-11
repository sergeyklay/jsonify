# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from bot import app


@pytest.fixture
def client():
    app_instance = app.create_app('testing')
    with app_instance.test_client() as client:
        yield client

