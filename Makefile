# Generate themefiles for base16 templates
# Execute inside repo root directory
# Adapted from: https://github.com/theova/base16-qutebrowser

BUILD=base16
REPO=$(shell pwd)
THEME_DIR=themes
BASE16_DIR=$(REPO)/base16
TEMP_DIR=$(BASE16_DIR)/templates/base16-pyradio
OUTPUT=out

all: update build

update:
	mkdir -p $(BASE16_DIR)
	rm -rf $(BASE16_DIR)/schemes
	git clone https://github.com/base16-project/base16-schemes.git $(BASE16_DIR)/schemes

build:
	mkdir -p $(TEMP_DIR)
	ln -sfn $(REPO)/templates/ $(TEMP_DIR)
	base16 build
	rm -rf $(THEME_DIR)
	mv $(TEMP_DIR)/themes $(REPO)
	
