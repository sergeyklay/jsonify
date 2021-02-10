# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from bot.json import JsonDecoder


@pytest.mark.parametrize(
    'provided,expected',
    [
        ('{}', []),
        ('[1, 2, 3, 4]', []),
        ('{"a": [1], "b": 42, "c": {"c1": 7, "c2": [1, 2]}}', ['a', 'c.c2']),
    ])
def test_list_paths(provided, expected):
    """Create paths of all nested dictionary values."""
    decoder = JsonDecoder(provided)

    actual = decoder.list_paths()
    actual.sort()

    assert actual == expected

