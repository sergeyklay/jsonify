# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import request

from bot import logger
from bot.api import api
from bot.exceptions import BadRequest


@api.route('/events/handle', methods=['POST'])
def event_handle():
    """Gets all trigger related events."""
    contents = request.get_json()
    logger.info('Received webhook. Event data: %s' % contents)

    if not isinstance(contents, dict):
        raise BadRequest('No input data provided')

    # TODO:
    # 1. Create processor
    # 2. Pass contents to processor
    # 3. Process the data
    # 4. Return value to views
    # 5. Create response

    return {}
