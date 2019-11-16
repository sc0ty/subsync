SCRIPTS_DIR = scripts

URL ?= https://github.com/sc0ty/subsync/releases/download/assets/
URL_LOCAL ?= http://localhost:8000/assets/

DICT_DIR   = dict
SPEECH_DIR = speech
EXTRA_DIR  = extra

ASSET_DIR  = assets
SPEC_DIR   = specs

DICTS    = $(wildcard $(DICT_DIR)/*.dict)
SPEECHES = $(wildcard $(SPEECH_DIR)/*.speech)
EXTRAS   = $(wildcard $(EXTRA_DIR)/*.json)

DICT_ASSETS   = $(patsubst $(DICT_DIR)/%.dict,$(ASSET_DIR)/dict-%.zip,$(DICTS))
SPEECH_ASSETS = $(patsubst $(SPEECH_DIR)/%.speech,$(ASSET_DIR)/speech-%.zip,$(SPEECHES))
EXTRA_ASSETS  = $(patsubst $(EXTRA_DIR)/%.json,$(ASSET_DIR)/%.zip,$(EXTRAS))

ASSETS = $(DICT_ASSETS) $(SPEECH_ASSETS) $(EXTRA_ASSETS)
SIGNS = $(addsuffix .asc,$(ASSETS))
INDEX = assets.json assets_local.json


all: $(ASSETS) $(SIGNS) $(INDEX)

clean:
	$(RM) -r $(ASSET_DIR)
	$(RM) -r $(SPEC_DIR)
	$(RM) $(INDEX)


$(DICT_ASSETS): $(ASSET_DIR)/dict-%.zip: $(DICT_DIR)/%.dict
	@mkdir -p $(ASSET_DIR)
	zip -q $@ $<

$(SPEECH_ASSETS): $(ASSET_DIR)/speech-%.zip: $(SPEECH_DIR)/%.speech
	@mkdir -p $(ASSET_DIR)
	zip -q --recurse-paths $@ $< $(addprefix $(SPEECH_DIR)/,$(notdir $(shell jq -cr .dir $<)))

$(EXTRA_ASSETS): $(ASSET_DIR)/%.zip: $(EXTRA_DIR)/%.zip $(EXTRA_DIR)/%.json
	@mkdir -p $(ASSET_DIR)
	cp $< $@


$(SIGNS): %.asc: %
	$(SCRIPTS_DIR)/sign.py $< $@ key.pem

assets.json: $(ASSETS) $(SIGNS)
	$(SCRIPTS_DIR)/mkindex.py $(URL) $(ASSET_DIR) $(EXTRA_DIR) $@

assets_local.json: $(ASSETS) $(SIGNS)
	$(SCRIPTS_DIR)/mkindex.py $(URL_LOCAL) $(ASSET_DIR) $(EXTRA_DIR) $@

.PHONY: all clean
