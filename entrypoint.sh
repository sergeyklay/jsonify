#!/bin/sh
#
# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

set -e

show_help() {
    echo """
Usage: docker run <imagename> COMMAND

Available commands:

  help:         Show this help and exit
  dev:          Start a normal Flask development server
"""
}

case "$1" in
  dev)
    echo "Running Development Server..."

    export FLASK_DEBUG=1
    export FLASK_ENV=development

    flask run --port 5000 --host 0.0.0.0
  ;;
  *)
    show_help
  ;;
esac
