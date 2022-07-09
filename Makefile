# Generate themefiles for base16 templates
# Execute inside repo root directory
# Adapted from: https://github.com/theova/base16-qutebrowser

BUILD=base16
BASE16_DIR=../..

all: update build

update:
	rm -rf $(BASE16_DIR)/schemes
	git clone https://github.com/base16-project/base16-schemes.git $(BASE16_DIR)/schemes

build:
	cd ../../.. && $(BUILD) build base16 --prefix base16-
	
