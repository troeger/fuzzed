THEME=white

CSS_DIR=front/FuzzEd/static/css
LESS_DIR=front/FuzzEd/static/less
MODELS_DIR=front/FuzzEd/models
XSD_DIR=front/FuzzEd/static/xsd
XSD_FILES=common configurations backend fuzztree faulttree
PYXBGEN_TARGETS=$(foreach xsd_file,$(XSD_FILES),$(MODELS_DIR)/xml_$(xsd_file).py)
PYXBGEN_ARGS=$(foreach xsd_file,$(XSD_FILES),-u $(XSD_DIR)/$(xsd_file).xsd -m xml_$(xsd_file))

types= ham cheese salad
what = $(foreach a, $(types), john likes $(a) )


ORE_FRONT_RUN=docker run -i -t --rm --mount source=$(PWD),target=/ore,type=bind -p 127.0.0.1:8000:8000 

all: $(CSS_DIR)/theme/$(THEME).css $(PYXBGEN_TARGETS)

clean:
	rm -f $(PYXBGEN_TARGETS)
	rm -f $(CSS_DIR)/theme/$(THEME).css

$(CSS_DIR)/theme/$(THEME).css: $(LESS_DIR)/theme/$(THEME)/theme.less
	lessc $< $@

$(MODELS_DIR)/xml_%.py: $(XSD_DIR)/%.xsd
	pyxbgen --binding-root=$(MODELS_DIR) $(PYXBGEN_ARGS)

docker-front-image:
	cd front; docker build -t troeger/ore_front:latest .;cd ..

docker-back-image:
	cd back; docker build -t troeger/ore_back:latest .;cd ..

docker-images: docker-front-image docker-back-image

docker-shell: docker-front-image
	$(ORE_FRONT_RUN) -w /ore troeger/ore_front bash

docker-test: docker-front-image
	$(ORE_FRONT_RUN) -w /ore/front troeger/ore_front ./manage.py test

