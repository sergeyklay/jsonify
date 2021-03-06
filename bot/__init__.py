# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for the application.

This module tracks the version of the application as well as the
base application info used by various functions within the
package and provides a factory function to create application
instance.

Misc variables:

    __author__
    __author_email__
    __copyright__
    __description__
    __license__
    __url__
    __version__
    logger

"""

from flask import current_app
from werkzeug.local import LocalProxy

# TODO: Move outside or use builtin logger
logger = LocalProxy(lambda: current_app.logger)

__copyright__ = 'Copyright (C) 2021 Serghei Iakovlev'
__version__ = '1.0.0b1'
__license__ = 'Apache 2.0'
__author__ = 'Serghei Iakovlev'
__author_email__ = 'i.serghei@pdffiller.com'
__url__ = 'https://github.com/sergeyklay/as-jsonify-bot'
__description__ = 'A simple bot for developers.airslate.com'
