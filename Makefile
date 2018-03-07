VERSION=0.8.0

DOCKER_RUN=docker run -i -t --rm --mount source=$(PWD),target=/FuzzEd,type=bind -w /FuzzEd -p 127.0.0.1:8000:8000 troeger/ore_front:$(VERSION)

.PHONY=docker

all: build

docker-dev-image:
	docker build -t troeger/ore_front:$(VERSION) .

shell: docker-dev-image
	$(DOCKER_RUN) bash

build: docker-dev-image
	$(DOCKER_RUN) scons frontend backend

test: docker-dev-image build
	$(DOCKER_RUN) ./manage.py test

