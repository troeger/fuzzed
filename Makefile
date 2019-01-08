# Create docker images and start them
up:
	docker-compose up -d

# Stop docker images
down:
	docker-compose down

# Build frontend code in the running docker image
front-build: up
	docker exec -w /ore-front ore-front scons

# Build backend code in the running docker image
back-build: up
	docker exec -w /ore-back ore-back cmake .
	docker exec -w /ore-back ore-back make

# Build frontend and backend
build: front-build back-build

# Clean frontend build
front-clean: up
	docker exec ore-front /usr/bin/scons -C /ore-front -c

# Clean backend build
back-clean: up
	docker exec -w /ore-back ore-back make clean

# Clean frontend and backend build
clean: front-clean back-clean

# Get shell in running frontend docker image
front-shell: up
	docker exec -it ore-front bash

# Get shell in running backend docker image
back-shell: up
	docker exec -it ore-back bash

# Run test suite
test: up
	docker exec -w /ore-front ore-front python /ore-front/manage.py test
