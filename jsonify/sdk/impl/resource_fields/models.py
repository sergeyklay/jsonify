# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

class ResourceField:

    TYPE = 'slate-addon-variants'

    def __init__(self, filed_id=None, name=None, group_id=None, group_name=None):
        self._id = filed_id
        self._name = name
        self._group_id = group_id
        self._group_name = group_name

    def __repr__(self):
        return "<ResourceField: id='%s', name='%s'>" % (self.id, self.name)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def group_id(self):
        return self._group_id

    @property
    def group_name(self):
        return self._group_name

    def to_dict(self):
        result = {
            'id': self.id,
            'type': self.TYPE,
            'attributes': {
                'name': self.name
            },
        }

        if self.group_id is not None and self.group_name is not None:
            result['attributes']['group'] = {
                'id': self.group_id,
                'name': self.group_name,
            }

        return result
