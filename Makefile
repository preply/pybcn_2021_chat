.PHONY: run test revision upgrade downgrade bash build stop

COMPOSE-DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE-TEST = docker-compose -f docker-compose.yml -f docker-compose.test.yml


run:
	if [ ! -f .env ]; then cp .env.example .env; fi;
	$(COMPOSE-DEV) build
	$(COMPOSE-DEV) up --detach
	$(COMPOSE-DEV) exec chat alembic upgrade head

test:
	if [ ! -f .env ]; then cp .env.example .env; fi;
	TEST_FILE=$(file) $(COMPOSE-TEST) up --build --abort-on-container-exit

revision:
	$(COMPOSE-DEV) exec chat alembic revision --autogenerate -m $(name)

upgrade:
	$(COMPOSE-DEV) exec chat alembic upgrade head

merge-heads:
	$(COMPOSE-DEV) exec chat alembic merge heads -m merge_heads

downgrade:
	$(COMPOSE-DEV) exec chat alembic downgrade -1

bash:
	$(COMPOSE-DEV) exec chat /bin/sh

build:
	$(COMPOSE-DEV) build

stop:
	$(COMPOSE-DEV) down
