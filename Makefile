# Generate themefiles for base16 templates
# Execute inside repo root directory
# Adapted from: https://github.com/theova/base16-qutebrowser

BUILD=pybase16
REPO=$(shell pwd)
TEMPLATE=$(shell basename $(REPO))
THEME_DIR=themes
TEMPLATE_DIR=templates
OUTPUT=out

all: update build

update:
	$(BUILD) update

build:
	$(BUILD) build -t $(REPO) -o $(OUTPUT)
	rm -rf $(THEME_DIR)
	mv -f ${OUTPUT}/${TEMPLATE}/themes/ ${THEME_DIR}/
	rm -rf ${OUTPUT} ${TEMPLATE_DIR}/*/
	
