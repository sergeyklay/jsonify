# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from dataclasses import dataclass

from asdicts.dict import path

from .transformers import (
    field_to_resource_fields,
    documents_to_resource_fields,
    SettingsTransformer,
)
from .. import flow


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
        transformer = SettingsTransformer()

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
            # Create a list of supported documents for a given flow.
            return supported_documents(
                settings=request.settings,
                org_id=request.org_id,
                flow_id=request.flow_id
            )
        elif setting_name == 'documents_fields':
            # Create a list of supported document fields for a given flow.
            return supported_document_fields(
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


def supported_document_fields(settings: dict, org_id: str, flow_id: str):
    """Create a list of supported document fields for a given flow."""
    data_type = settings.get('data_type')
    field_types = supported_mapping(data_type)
    field_list = flow.field_list(org_id, flow_id, field_types)
    return field_to_resource_fields(field_list)


def supported_documents(settings: dict, org_id: str, flow_id: str):
    """Create a list of supported documents for a given flow."""
    data_type = settings.get('data_type')
    field_types = supported_mapping(data_type)
    doc_list = flow.document_list(org_id, flow_id, field_types)
    return documents_to_resource_fields(doc_list)
