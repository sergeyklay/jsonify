# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from app.sdk.collections import path


def extract_id(data: dict) -> str or None:
    """Extract Organization ID from given dictionary."""
    return path(data, 'relationships.organization.data.id')
