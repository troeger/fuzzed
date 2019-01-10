dev-build:
	docker-compose -f docker-compose.development.yml build
	docker-compose -f docker-compose.development.yml up -d
	docker exec -w /ore-front ore-front-dev scons
	docker exec -w /ore-back ore-back-dev cmake .
	docker exec -w /ore-back ore-back-dev make
	docker-compose -f docker-compose.development.yml down

dev-up:
	docker-compose -f docker-compose.development.yml up

dev-down:
	docker-compose -f docker-compose.development.yml down 

dev-clean:
	docker exec ore-front-dev /usr/bin/scons -C /ore-front -c
	docker exec -w /ore-back ore-back-dev make clean

dev-back-log:
	docker logs ore-back-dev -f

dev-front-log:
	docker logs ore-front-dev -f

dev-front-shell:
	docker exec -it ore-front-dev bash

dev-back-shell:
	docker exec -it ore-back-dev bash

prod-build:
	docker-compose -f docker-compose.production.yml build

prod-up:
	docker-compose -f docker-compose.production.yml up

prod-down:
	docker-compose -f docker-compose.production.yml down 




