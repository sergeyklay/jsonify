# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# This Makefile is designed to make it easier to work with Docker
# as well as Docker Compose only. For any other commands use
#   'flask <command>'.
#

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL    := $(shell which bash)

.env: .env.example
	cp $< $@

requirements/%.txt: requirements/%.in
	pip-compile --no-annotate --no-header --output-file $@ $<

## Public targets

.PHONY: build
build: .env requirements/requirements-docker.txt
	docker-compose build --force-rm app

.PHONY: up
up:
	docker-compose up -d

.PHONY: ps
ps:
	docker-compose ps

.PHONY: stop
stop:
	docker-compose stop

.PHONY: shell
shell:
	docker-compose exec app sh

.PHONY: down
down:
	docker-compose down -v --remove-orphans
	docker network prune -f

.PHONY: dist-clean
dist-clean: down
	$(RM) *.env
	$(RM) *.sqlite3
