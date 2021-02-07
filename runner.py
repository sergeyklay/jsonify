# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for Jsonify."""

import os

from bot.app import create_app, load_env_vars

load_env_vars(os.path.dirname(os.path.abspath(__file__)))

configuration = os.getenv('BOT_ENVIRONMENT', 'default').lower()
app = create_app(configuration)
