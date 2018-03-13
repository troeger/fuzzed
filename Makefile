ORE_FRONT_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -w /ore -p 127.0.0.1:8000:8000 troeger/ore_front

.PHONY=docker

all: build

docker-front-image:
	cd front; docker build -t troeger/ore_front:latest .;cd ..

docker-back-image:
	cd back; docker build -t troeger/ore_back:latest .;cd ..

docker-images: docker-front-image docker-back-image

front-shell: docker-front-image
	$(ORE_FRONT_RUN) bash

front-build: docker-front-image
	$(ORE_FRONT_RUN) scons frontend

front-test: docker-front-image
	$(ORE_FRONT_RUN) web/manage.py test

