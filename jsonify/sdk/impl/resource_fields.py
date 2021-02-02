# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from dataclasses import dataclass

from asdicts.dict import path

from . import flow, transformers


# TODO: Move to addon settings
def supported_mapping(data_type: str):
    if data_type == 'table':
        # Table fields
        return [
            'text[]',
            'number[]',
            'date[]'
        ]

    # Single line fields
    return [
        'text',
        'number',
        'date',
        'checkbox',
        'dropdown',
        'radiogroup'
    ]


@dataclass
class Request:
    org_id: str
    addon_id: str
    flow_id: str
    setting_name: str
    settings: dict

    @staticmethod
    def from_dict(data: dict):
        transformer = transformers.settings.SettingsTransformer()

        return Request(
            path(data, 'meta.organization.data.id'),
            path(data, 'data.relationships.organization_addon.data.id'),
            path(data, 'data.relationships.slate.data.id'),
            path(data, 'data.attributes.setting_name'),
            transformer.transform(path(data, 'data.attributes.settings')),
        )


class Response(dict):
    def __init__(self, fields):
        super().__init__(
            data=[field.to_dict() for field in fields]
        )


class Parser:
    def parse(self, request: Request):
        setting_name = str(request.setting_name)

        if setting_name == 'lists':
            return self._parse_lists(
                settings=request.settings,
                org_id=request.org_id,
            )
        elif setting_name == 'listed_objects_fields':
            return self._parse_listed_objects_fields(
                settings=request.settings,
                org_id=request.org_id,
            )
        elif setting_name == 'documents':
            return self._parse_documents(
                settings=request.settings,
                org_id=request.org_id,
                flow_id=request.flow_id
            )
        elif setting_name == 'documents_fields':
            return self._parse_documents_fields(
                settings=request.settings,
                org_id=request.org_id,
                flow_id=request.flow_id
            )
        else:
            return []

    def _parse_lists(self, settings: dict, org_id: str):
        # TODO: Implement me
        return []

    def _parse_listed_objects_fields(self, settings: dict, org_id: str):
        # TODO: Implement me
        return []

    def _parse_documents(self, settings: dict, org_id: str, flow_id: str):
        data_type = settings.get('data_type')
        field_types = supported_mapping(data_type)
        doc_list = flow.document_list(org_id, flow_id, field_types)
        return create_from_document_list(doc_list)

    def _parse_documents_fields(self, settings: dict, org_id: str, flow_id: str):
        # TODO: Implement me
        return []


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


def create_from_document_list(doc_list) -> [ResourceField]:
    result = []

    for document in doc_list:
        field = ResourceField(
            filed_id=path(document, 'id'),
            name=path(document, 'name'),
        )
        result.append(field)

    return result
