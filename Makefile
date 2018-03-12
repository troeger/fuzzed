ORE_FRONT_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -w /ore -p 127.0.0.1:8000:8000 troeger/ore_front

.PHONY=docker

all: build

docker-images:
	docker-compose build

shell: docker-images
	$(ORE_FRONT_RUN) bash

build: docker-images
	$(ORE_FRONT_RUN) scons frontend backend

test: docker-images build
	$(ORE_FRONT_RUN) ./manage.py test

