# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

class BaseResource:
    TYPE = 'slate-addon-variants'

    def __init__(self, rf_id=None, name=None):
        self._id = rf_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class DocumentResourceField(BaseResource):
    def __init__(self, rf_id=None, name=None, type_name=None,
                 doc_id=None, doc_name=None):
        super().__init__(rf_id, name)
        self._type = type_name
        self._doc_id = doc_id
        self._doc_name = doc_name

    def __repr__(self):
        return "<DocumentResourceField: id='%s', name='%s'>" % (
            self.id, self.name
        )

    @property
    def type(self):
        return self._type

    @property
    def document_id(self):
        return self._doc_id

    @property
    def document_name(self):
        return self._doc_name

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.TYPE,
            'attributes': {
                'name': self.name,
                'icon_type': self.type or 'default',
                'group': {
                    'id': self.document_id,
                    'name': self.document_name,
                }
            },
        }


class ResourceField(BaseResource):
    def __init__(self, rf_id=None, name=None, group_id=None, group_name=None):
        super().__init__(rf_id, name)
        self._group_id = group_id
        self._group_name = group_name

    def __repr__(self):
        return "<ResourceField: id='%s', name='%s'>" % (self.id, self.name)

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
