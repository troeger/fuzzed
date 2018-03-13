ORE_FRONT_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -p 127.0.0.1:8000:8000 

.PHONY=docker

all: build

docker-front-image:
	cd front; docker build -t troeger/ore_front:latest .;cd ..

docker-back-image:
	cd back; docker build -t troeger/ore_back:latest .;cd ..

docker-images: docker-front-image docker-back-image

front-shell: docker-front-image
	$(ORE_FRONT_RUN) -w /ore troeger/ore_front bash

front-build: docker-front-image
	$(ORE_FRONT_RUN) -w /ore troeger/ore_front scons frontend

front-test: docker-front-image
	$(ORE_FRONT_RUN) -w /ore/front troeger/ore_front ./manage.py test

