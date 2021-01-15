# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL    := $(shell which bash)

.env: .env.example
	cp $^ $@

## Public targets

.PHONY: build
build: .env
	@docker-compose build --force-rm app

.PHONY: up
up:
	@docker-compose up -d

.PHONY: ps
ps:
	@docker-compose ps

.PHONY: stop
stop:
	@docker-compose stop

.PHONY: clean
clean:
	@docker-compose down -v --remove-orphans
	@docker network prune -f

.PHONY: dist-clean
dist-clean: clean
	@$(RM) .env
