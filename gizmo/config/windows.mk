LIB_SUFFIX   ?= .pyd

CXXFLAGS += \
			 -I$(POCKETSPHINX)\include \
			 -I$(SPHINXBASE)\include \
			 -I$(SPHINXBASE)\include\win32 \
			 -I$(FFMPEG)\include \
			 -D__STDC_CONSTANT_MACROS

LDFLAGS  += \
			 -lsphinxbase \
			 -lpocketsphinx \
			 -L$(POCKETSPHINX)\bin\Release\x64 \
			 -L$(SPHINXBASE)\bin\Release\x64 \
			 -lavdevice \
			 -lavformat \
			 -lavfilter \
			 -lavcodec \
			 -lswresample \
			 -lswscale \
			 -lavutil \
			 -L$(FFMPEG)\lib \
			 $(PYTHONLIB) \

CXXFLAGS += $(shell python -m pybind11 --includes)
