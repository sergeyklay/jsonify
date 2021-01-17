# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The api blueprint module for the application."""

from flask import Blueprint

api = Blueprint('api', __name__)

from . import organizations
