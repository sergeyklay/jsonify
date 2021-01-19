# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import unittest

from app.sdk import collections


class TestCollections(unittest.TestCase):

    def test_path(self):
        my_dict = {'a': {'b': {'c': {'d': 42}}}}

        self.assertEqual(collections.path(my_dict, 'a'), {'b': {'c': {'d': 42}}})
        self.assertEqual(collections.path(my_dict, 'a.b'), {'c': {'d': 42}})
        self.assertEqual(collections.path(my_dict, 'a.b.c'), {'d': 42})
        self.assertEqual(collections.path(my_dict, 'a.b.c.d'), 42)
        self.assertIsNone(collections.path(my_dict, 'a.z.c.d'))
        self.assertIsNone(collections.path(my_dict, 'a.b.c.z'))
        self.assertIsNone(collections.path(my_dict, 'z.y.z'))
        self.assertIsNone(collections.path(my_dict, '42'))

    def test_merge(self):
        self.assertEqual(
            collections.merge({'a': 42}, {'foo': 'bar'}),
            {'a': 42, 'foo': 'bar'}
        )

        self.assertEqual(
            collections.merge({'a': 42}, {'foo': 'bar', 'a': 17}),
            {'a': 17, 'foo': 'bar'}
        )

        self.assertEqual(
            collections.merge({'a': 17, 'foo': 'bar'}),
            {'a': 17, 'foo': 'bar'}
        )

        self.assertEqual(
            collections.merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 4}),
            {'a': 4, 'b': 2, 'c': 3}
        )
