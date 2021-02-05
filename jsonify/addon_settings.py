# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

TABLE_FIELDS = [
    'text[]',
    'number[]',
    'date[]',
]

SINGLE_LINE_FIELDS = [
    'text',
    'number',
    'date',
    'checkbox',
    'dropdown',
    'radiogroup',
]

def supported_mapping(data_type: str):
    if data_type == 'table':
        return TABLE_FIELDS
    return SINGLE_LINE_FIELDS
