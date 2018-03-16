THEME=white

ROOT_DIR=FuzzEd

CSS_DIR=$(ROOT_DIR)/static/css
LESS_DIR=$(ROOT_DIR)/static/less
XSD_DIR=$(ROOT_DIR)/static/xsd
JQUI_DIR=$(ROOT_DIR)/static/lib/jquery-ui
IMG_DIR=$(ROOT_DIR)/static/img
NOTATIONS_DIR=$(ROOT_DIR)/static/notations
MODELS_DIR=$(ROOT_DIR)/models
FAWS_DIR=$(CSS_DIR)/font-awesome

XSD_FILES=common configurations backend fuzztree faulttree

PYXBGEN_TARGETS=$(foreach xsd_file,$(XSD_FILES),$(MODELS_DIR)/xml_$(xsd_file).py)

PATCH_TARGETS=$(FAWS_DIR)/font-awesome-4.1.0.css \
              $(FAWS_DIR)/font-awesome-4.1.0.min.css \
              $(JQUI_DIR)/jquery-ui-1.10.3.js \
              $(JQUI_DIR)/jquery-ui-1.10.3.min.js

TARGETS=$(CSS_DIR)/theme/$(THEME).css \
        $(PYXBGEN_TARGETS) \
        $(PATCH_TARGETS) \
        $(MODELS_DIR)/node_rendering.py \
        $(MODELS_DIR)/notations.py 

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

# Generate the frontend CSS
$(CSS_DIR)/theme/$(THEME).css: $(LESS_DIR)/theme/$(THEME)/theme.less
	lessc $< $@

# Generate XML binding classes for the project XSDs
$(MODELS_DIR)/xml_%.py: $(XSD_DIR)/%.xsd
	pyxbgen --module-prefix=FuzzEd.models $(foreach xsd_file,$(XSD_FILES),-u $(XSD_DIR)/$(xsd_file).xsd -m xml_$(xsd_file))

# Generate a large Python string with TiKZ code for the SVG images in models
$(MODELS_DIR)/node_rendering.py: $(shell find $(IMG_DIR)/*/ -type f -name '*.svg')
	python3 -m FuzzEd.build tikz $@ $^

# Generate a Python represenation of all Graph type configuration
$(MODELS_DIR)/notations.py: $(shell find $(NOTATIONS_DIR) -type f -name '*.json')
	python3 -m FuzzEd.build notations $@ $^

# Some 3rd party files must be patched for this project
$(PATCH_TARGETS): %: %.patch
	patch -o $@ $@.orig $<
