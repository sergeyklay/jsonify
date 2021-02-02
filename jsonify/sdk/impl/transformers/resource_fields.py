# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from asdicts.dict import path

from jsonify.sdk.impl.resource_fields import models


def documents_to_resource_fields(documents):
    result = []

    for document in documents:
        field = models.ResourceField(
            filed_id=path(document, 'id'),
            name=path(document, 'name'),
        )
        result.append(field)

    return result
