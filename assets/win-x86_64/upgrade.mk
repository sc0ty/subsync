WIN64_DIR = win-x86_64
WIN64_UPGRADE_DIR = $(WIN64_DIR)/upgrade

version = $(word 2,$(subst -, ,$(notdir $1)))

WIN64_SRC_INSTALLER = $(wildcard $(WIN64_DIR)/subsync-*.msi)
WIN64_INSTALLER = $(patsubst $(WIN64_DIR)/subsync-%.msi,$(WIN64_UPGRADE_DIR)/subsync-%.msi,$(WIN64_SRC_INSTALLER))
WIN64_ASSET = $(ASSET_DIR)/subsync-$(call version,$(WIN64_INSTALLER))-win-x86_64.zip

ASSETS += $(WIN64_ASSET)


all:

clean: clean_win64


$(WIN64_ASSET): $(WIN64_INSTALLER) $(WIN64_UPGRADE_DIR)/install.cmd $(WIN64_UPGRADE_DIR)/upgrade.json
	@mkdir -p $(ASSET_DIR)
	cd $(WIN64_DIR) ; zip -q --recurse-paths ../$@ $(patsubst $(WIN64_DIR)/%,%,$^)

$(WIN64_INSTALLER): $(WIN64_SRC_INSTALLER)
	@mkdir -p $(WIN64_UPGRADE_DIR)
	$(RM) $(WIN64_UPGRADE_DIR)/subsync-*.msi
	cp $< $@

$(WIN64_UPGRADE_DIR)/install.cmd: $(WIN64_INSTALLER)
	@mkdir -p $(WIN64_UPGRADE_DIR)
	echo start msiexec.exe /i $(notdir $<) > $@

$(WIN64_UPGRADE_DIR)/upgrade.json: $(WIN64_INSTALLER)
	@mkdir -p $(WIN64_UPGRADE_DIR)
	echo '{"version": "$(call version,$<)", "install": "install.cmd"}' > $@

clean_win64:
	$(RM) -r $(WIN64_UPGRADE_DIR)

.PHONY: clean_win64
