# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

.PHONY: build
build:
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
