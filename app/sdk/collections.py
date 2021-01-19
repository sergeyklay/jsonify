# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
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
    >>> path(d, 'rel.org.data.foo')
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


def merge(*objects):
    """Merge one or more objects into a new object.

    >>> merge({'a': 42}, {'foo': 'bar'})
    {'a': 42, 'foo': 'bar'}
    >>> merge({'a': 42}, {'foo': 'bar', 'a': 17})
    {'a': 17, 'foo': 'bar'}
    >>>  merge({'a': 17, 'foo': 'bar'})
    {'a': 17, 'foo': 'bar'}
    >>> merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 4})
    {'a': 4, 'b': 2, 'c': 3}
    """
    result = {}
    [result.update(obj) for obj in objects]

    return result
