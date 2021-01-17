# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from . import api


@api.route('/resource/fields', methods=['POST'])
def resource_fields():
    raise NotImplementedError()


@api.route('/resource/settings', methods=['POST'])
def resource_settings():
    raise NotImplementedError()
