# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

class BaseResource:
    TYPE = 'slate-addon-variants'

    def __init__(self, resource_id=None, name=None):
        self._resource_id = resource_id
        self._name = name

    @property
    def id(self):
        return self._resource_id

    @property
    def name(self):
        return self._name


class Document(BaseResource):
    def __init__(self, resource_id=None, name=None, resource_type=None,
                 document_id=None, document_name=None):
        super().__init__(resource_id, name)
        self._resource_type = resource_type
        self._document_id = document_id
        self._document_name = document_name

    def __repr__(self):
        return "<Document: id='%s', name='%s'>" % (self.id, self.name)

    @property
    def type(self):
        return self._resource_type

    @property
    def document_id(self):
        return self._document_id

    @property
    def document_name(self):
        return self._document_name

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


class Field(BaseResource):
    def __init__(self, rf_id=None, name=None, group_id=None, group_name=None):
        super().__init__(rf_id, name)
        self._group_id = group_id
        self._group_name = group_name

    def __repr__(self):
        return "<Field: id='%s', name='%s'>" % (self.id, self.name)

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
