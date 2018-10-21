PYTHON_PREFIX ?= python

WXFORMBUILDER ?= wxformbuilder
UPDATE_TRANSLATIONS ?= PYTHONPATH=. $(PYTHON_PREFIX) ../tools/update_translations.py

GUI_SRC = \
		  gui/mainwin.fbp \
		  gui/subpanel.fbp \
		  gui/openwin.fbp \
		  gui/syncwin.fbp \
		  gui/settingswin.fbp \
		  gui/downloadwin.fbp \
		  gui/aboutwin.fbp \
		  gui/errorwin.fbp \

GUI_DST = $(GUI_SRC:.fbp=_layout.py)


all: gui-gen config.py version.py

clean: gui-gen-clean version-clean


gui-gen: $(GUI_DST)

gui-gen-clean:
	$(RM) $(GUI_DST)
	$(RM) $(GUI_DST:.py=.py.tmp)

$(GUI_DST): %_layout.py: %.fbp
	$(WXFORMBUILDER) -g $<


config.py:
	cp config.py.template $@

version.py: .FORCE
	$(PYTHON_PREFIX) ../tools/update_version.py $@

version-clean:
	$(RM) version.py


translations:
	$(UPDATE_TRANSLATIONS)


.PHONY: all clean gui-gen gui-gen-clean version-clean translations
.PHONY: .FORCE
