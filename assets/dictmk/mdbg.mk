MDBG_TEMP_DIR = $(TEMP_DIR)/mdbg
MDBG_PART_DIR = $(PART_DIR)/mdbg
PARTS += $(MDBG_PART_DIR)

MDBG_GZ  = $(MDBG_TEMP_DIR)/mdbg.txt.gz
MDBG_TXT = $(MDBG_TEMP_DIR)/mdbg.txt


download: $(MDBG_GZ)
extract: $(MDBG_TXT)
convert: mdbg


mdbg: $(MDBG_TXT)
	@mkdir -p $(MDBG_PART_DIR)
	$(SCRIPTS_DIR)/mdbg_convert.py $< $(MDBG_PART_DIR) $(DICT_VERSION)

$(MDBG_GZ):
	@mkdir -p $(MDBG_TEMP_DIR)
	wget -nv -O $@ https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz

$(MDBG_TXT): $(MDBG_GZ)
	gunzip -fk $<
