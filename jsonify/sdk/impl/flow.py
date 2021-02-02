# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from airslate.client import Client
from airslate.entities.documents import Document

from jsonify.sdk.impl.client_factory import create_client


def document_list(org_id: str, flow_id: str, fields_types=None):
    """Create a list of documents ids and names from a given flow."""
    documents = get_documents(flow_id, create_client(org_id))

    if fields_types is not None:
        documents = _filter_documents(documents, fields_types)

    return [{'id': doc['id'], 'name': doc['name']} for doc in documents]


def get_documents(flow_id: str, client: Client):
    """Get supported documents for given flow."""
    return client.flow_documents.collection(flow_id, include='fields')


def _filter_documents(documents: [Document], filed_types):
    """Filter the list of documents with fields from ``filed_types``."""
    result = []

    for document in documents:
        for field in document.fields:
            if field['field_type'] in filed_types:
                result.append(document)
                break

    return result
