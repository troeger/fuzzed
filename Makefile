build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

front-shell: up
	docker-compose exec front bash

back-shell: up
	docker-compose exec back bash

clean: up
	docker-compose exec front /usr/bin/scons -C /ore-front -c
