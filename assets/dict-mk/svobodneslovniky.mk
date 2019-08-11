SVOB_TEMP_DIR = $(TEMP_DIR)/svob
SVOB_PART_DIR = $(PART_DIR)/svob

SVOB_BZ2 = $(SVOB_TEMP_DIR)/svob.txt.bz2
SVOB_TXT = $(SVOB_TEMP_DIR)/svob.txt


download: $(SVOB_BZ2)
extract: $(SVOB_TXT)
convert: svob


svob: $(SVOB_TXT)
	@mkdir -p $(SVOB_PART_DIR)
	$(SCRIPTS_DIR)/svobodneslovniky_convert.py $< $(SVOB_PART_DIR) $(DICT_VERSION)

$(SVOB_BZ2):
	@mkdir -p $(SVOB_TEMP_DIR)
	wget -nv -O $@ https://www.svobodneslovniky.cz/data/en-cs.txt.bz2

$(SVOB_TXT): $(SVOB_BZ2)
	bunzip2 -fk $<
