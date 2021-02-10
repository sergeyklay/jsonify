#!/bin/sh
#
# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

set -e

# Export environment variables early to be able run 'flask deploy'
# w/o initializing whole application and properly initializing
# configuration class.
if [ -f ./.env ]; then
  . ./.env
  export $(cut -d= -f1 ./.env | grep -v "^#\|^$")
fi

interval=0
retries=0

while ! flask deploy; do
  interval=$((interval+3))
  retries=$((retries+1))

  if [ $retries -lt 10 ] ; then
    echo "Deploy command failed, retrying in $interval secs..."
    sleep $interval
  else
    >&2 echo "Deploy command failed after $retries attempts."
    >&2 echo "Aborting."
    exit 1
  fi
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - runner:bot
