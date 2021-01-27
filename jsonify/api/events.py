# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from jsonify.api import api


@api.route('/events/handle', methods=['POST'])
def event_handle():
    """Gets all trigger related events."""
    raise NotImplementedError()
