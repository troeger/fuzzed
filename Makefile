dev-build:
	docker-compose build
	docker-compose up -d
	docker exec -w /ore-front ore-front-dev scons
	docker exec -w /ore-back ore-back-dev cmake .
	docker exec -w /ore-back ore-back-dev make
	docker-compose down

dev-up:
	docker-compose up

dev-down:
	docker-compose down 

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

prod-build: dev-build
	# Use dev containers to build neccessary files
	docker-compose up -d
	docker exec -w /ore-front ore-front-dev ./manage.py collectstatic --noinput --configuration=Dev
	docker-compose down
	# Build production containers
	docker build -t troeger/ore-front:0.8.0 -f frontend/docker/Dockerfile.production .
	docker build -t troeger/ore-back:0.8.0 -f backends/docker/Dockerfile.production .

prod-push:
	docker login
	docker push troeger/ore-front:0.8.0 
	docker push troeger/ore-back:0.8.0 
