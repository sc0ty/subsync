DICTS_DIR = ../dict
TEMP_DIR = temp
PART_DIR = part
SCRIPTS_DIR = scripts
PARTS =

DICT_VERSION ?= 1.1.0
DICT_MINKEYS ?= 10000


all: merge

download:

extract:

convert:

merge: convert
	@mkdir -p $(DICTS_DIR)
	$(SCRIPTS_DIR)/merge_dicts.py $(PARTS) $(DICTS_DIR) $(DICT_MINKEYS)

clean:
	$(RM) -r $(DICTS_DIR)
	$(RM) -r $(TEMP_DIR)
	$(RM) -r $(PART_DIR)


.PHONY: all download extract convert merge clean

include wiktionary.mk
include wikdict.mk
include iate.mk
include svobodneslovniky.mk
include mdbg.mk
