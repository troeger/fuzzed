build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

front-shell: up
	docker exec -it ore-front bash

back-shell: up
	docker exec -it ore-back bash

clean: up
	docker exec ore-front /usr/bin/scons -C /ore-front -c

test: up
	docker exec -w /ore-front ore-front python /ore-front/manage.py test
