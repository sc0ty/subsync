SCRIPTS_DIR = scripts

URL ?= https://github.com/sc0ty/subsync/releases/download/assets/
URL_LOCAL ?= http://localhost:8000/assets/

DICT_DIR = dict
SPEECH_DIR = speech
ASSET_DIR = assets

DICTS = $(wildcard $(DICT_DIR)/*.dict)
SPEECHES = $(wildcard $(SPEECH_DIR)/*.speech)

DICT_ASSETS = $(patsubst $(DICT_DIR)/%.dict,$(ASSET_DIR)/dict-%.zip,$(DICTS))
SPEECH_ASSETS = $(patsubst $(SPEECH_DIR)/%.speech,$(ASSET_DIR)/speech-%.zip,$(SPEECHES))

ASSETS = $(DICT_ASSETS) $(SPEECH_ASSETS)
SIGNS = $(addsuffix .asc,$(ASSETS))
INDEX = assets.json assets_local.json


include win-x86_64/upgrade.mk

all: $(ASSETS) $(SIGNS) $(INDEX)

clean:
	$(RM) -r $(ASSET_DIR)
	$(RM) $(INDEX)


$(DICT_ASSETS): $(ASSET_DIR)/dict-%.zip: $(DICT_DIR)/%.dict
	@mkdir -p $(ASSET_DIR)
	zip -q $@ $<

$(SPEECH_ASSETS): $(ASSET_DIR)/speech-%.zip: $(SPEECH_DIR)/%.speech
	@mkdir -p $(ASSET_DIR)
	zip -q --recurse-paths $@ $< $(addprefix $(SPEECH_DIR)/,$(notdir $(shell jq -cr .dir $<)))

$(SIGNS): %.asc: %
	$(SCRIPTS_DIR)/sign.py $< $@ key.pem

assets.json: $(ASSETS) $(SIGNS)
	$(SCRIPTS_DIR)/mkindex.py $(ASSET_DIR) $@ $(URL)

assets_local.json: $(ASSETS) $(SIGNS)
	$(SCRIPTS_DIR)/mkindex.py $(ASSET_DIR) $@ $(URL_LOCAL)

.PHONY: all clean
