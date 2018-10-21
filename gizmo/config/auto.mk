ifeq ($(OS),Windows_NT)
	include config/windows.mk
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		include config/linux.mk
	else ifeq ($(UNAME_S),Darwin)
		include config/macos.mk
	else
$(error cannot detect architecture, you must select configuration manually)
    endif
endif
