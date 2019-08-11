IATE_TEMP_DIR = $(TEMP_DIR)/iate
IATE_PART_DIR = $(PART_DIR)/iate

IATE_GZ = $(IATE_TEMP_DIR)/iate.xml.gz
IATE_XML = $(IATE_TEMP_DIR)/iate.xml


download: $(IATE_GZ)
extract: $(IATE_XML)
convert: iate


iate: $(IATE_XML)
	@mkdir -p $(IATE_PART_DIR)
	$(SCRIPTS_DIR)/iate_convert.py $< $(IATE_PART_DIR) $(DICT_VERSION)

$(IATE_GZ):
	@mkdir -p $(IATE_TEMP_DIR)
	wget -nv -O $@ https://iate.europa.eu/em-api/artifacts/full-tbx

$(IATE_XML): $(IATE_GZ)
	gunzip -fk $<
