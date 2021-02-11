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
def test_decoder_list_paths(provided, expected):
    """Create paths of all nested dictionary values."""
    decoder = JsonDecoder(provided)

    actual = decoder.list_paths()
    actual.sort()

    assert actual == expected


@pytest.mark.parametrize(
    'provided,path,expected',
    [
        ('{}', '', []),
        ('{}', 'a', []),
        ('{}', 'a.b', []),
        ('{"a": {"c": [1, 2]}, "b": [3, 4]}', 'a', ['c']),
        ('{"a": {"c": [1, 2]}, "b": [3, 4]}', 'b', []),
        ('{"a": {"c": [1, 2]}, "b": [3, 4]}', 'a.c', []),
        ('{"a": {"c": {"k1": "v1", "k2": "v2"}}}', 'a.c', ['k1', 'k2']),
        ('{"a": {"c": {"k1": "v1", "k2": "v2"}}}', 'x.y', []),
    ])
def test_decoder_fields(provided, path, expected):
    decoder = JsonDecoder(provided)

    actual = list(decoder.fields(path))
    actual.sort()

    assert actual == expected
