PYTHON_PREFIX ?= python

WXFORMBUILDER ?= wxformbuilder

GUI_SRC = \
		  gui/layout/mainwin.fbp \
		  gui/layout/subpanel.fbp \
		  gui/layout/openwin.fbp \
		  gui/layout/syncwin.fbp \
		  gui/layout/fpswin.fbp \
		  gui/layout/channelswin.fbp \
		  gui/layout/settingswin.fbp \
		  gui/layout/downloadwin.fbp \
		  gui/layout/aboutwin.fbp \
		  gui/layout/errorwin.fbp \

GUI_DST = $(GUI_SRC:.fbp=.py)


all: gui-gen config.py version.py

clean: gui-gen-clean version-clean


gui-gen: $(GUI_DST)

gui-gen-clean:
	$(RM) $(GUI_DST)

$(GUI_DST): %.py: %.fbp
	$(WXFORMBUILDER) -g $<
	$(PYTHON_PREFIX) ../tools/remove_gettext.py $@

config.py:
	cp config.py.template $@

version.py: .FORCE
	$(PYTHON_PREFIX) ../tools/update_version.py $@

version-clean:
	$(RM) version.py


.PHONY: all clean gui-gen gui-gen-clean version-clean translations
.PHONY: .FORCE
