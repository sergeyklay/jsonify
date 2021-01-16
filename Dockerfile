# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

## base image
FROM python:3.10-rc-alpine AS compile-image

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

## add and install requirements
RUN pip install --upgrade pip wheel
COPY requirements requirements
RUN pip install -r requirements/requirements-docker.txt

## build-image
FROM python:3.10-rc-alpine AS runtime-image

## set environment variables
ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_APP=jsonify.py

## copy Python dependencies from build image
COPY --from=compile-image /opt/venv /opt/venv

## set working directory
WORKDIR /usr/src/app

## add user
RUN addgroup --system user && adduser -S -D -H -G user user
RUN chown -R user:user /usr/src/app && chmod 755 /usr/src/app

## add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

## switch to non-root user
USER user

## add app
COPY . /usr/src/app

EXPOSE 5000

## run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
