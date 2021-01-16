# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The routes module for the application."""

from . import main


@main.route('/')
def index():
    return 'Hello, World!'
