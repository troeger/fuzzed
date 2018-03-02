VERSION = 0.8.0
XSD_TARGETS := $(addprefix FuzzEd/models/xml/, common.py configurations.py backend.py faulttree.py fuzztree.py)

all: css $(XSD_TARGETS) 

css: FuzzEd/static/css/theme/white.css

FuzzEd/models/xml/%.py: FuzzEd/static/xsd/%.xsd
	pyxbgen --binding-root=FuzzEd/models/xml/ -u $< -m $*

FuzzEd/static/css/theme/white.css: FuzzEd/static/less/theme/white/theme.less
	lessc $? $@

clean:
	rm -f FuzzEd/static/css/theme/white.css
	rm -f FuzzEd/models/xml/*

# Create a Docker image for local development
docker-dev-build:
	docker build -t troeger/ore_front:$(VERSION) .

# Run Docker image for local development
docker-dev:
	docker run -i -t --rm -v $(PWD):/FuzzEd -w /FuzzEd -p 127.0.0.1:8000:8000 troeger/ore_front:$(VERSION) bash
