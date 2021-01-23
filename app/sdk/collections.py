# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provide helpers to work with collection-like objects.

Functions:

    path(data: dict, item, default=None) -> Any

"""

from functools import reduce


def path(data: dict, item, default=None):
    """Steps through an item chain to get the ultimate value.

    If ultimate value or path to value does not exist, does not raise
    an exception and instead returns ``default``.

    >>> d = {'rel': {'org': {'data': {'id': 42}}}}
    >>> path(d, 'rel.org.data.id')
    42
    >>> path(d, 'foo.bar.baz.buz', 42)
    42
    >>> path(d, 'foo.bar.baz.buz')
    >>>
    """
    def getitem(obj, name: str):
        if obj is None:
            return default

        try:
            return obj[name]
        except (KeyError, TypeError):
            return default

    return reduce(getitem, item.split('.'), data)
