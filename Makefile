DOCKER_FRONT_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -p 127.0.0.1:8000:8000 
DOCKER_BACK_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -p 127.0.0.1:8000:8000 

all: docker-front-build docker-back-build

docker-front-build: docker-front-image 
	$(DOCKER_FRONT_RUN) -w /ore/front troeger/ore_front make

docker-back-build: docker-back-image
	$(DOCKER_BACK_RUN) -w /ore/back troeger/ore_back make

# Run the test suite in the Docker images
# ToDo: Test cases that need a backend daemon are currently excluded
docker-test: docker-front-image docker-front-build
	$(DOCKER_FRONT_RUN) -w /ore/front troeger/ore_front ./manage.py test --exclude-tag=back

# Generate a Docker image for the web frontend
docker-front-image:
	cd front; docker build -t troeger/ore_front:latest .;cd ..

# Generate a Docker image for the analysis backend
docker-back-image:
	cd back; docker build -t troeger/ore_back:latest .;cd ..

# Start a shell in a recent Docker image of the web frontend
docker-front-shell: docker-front-image
	$(DOCKER_FRONT_RUN) -w /ore/front troeger/ore_front bash

# Start a shell in a recent Docker image of the backend
docker-back-shell: docker-back-image
	$(DOCKER_BACK_RUN) -w /ore/back troeger/ore_back bash

