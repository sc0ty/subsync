PYTHON_PREFIX ?= python

LIBS += \
		pocketsphinx \
		sphinxbase \
		libavdevice \
		libavformat \
		libavfilter \
		libavcodec \
		libswresample \
		libswscale \
		libavutil \

CXXFLAGS += $(shell pkg-config --cflags $(LIBS))
LDFLAGS  += $(shell pkg-config --libs $(LIBS))

CXXFLAGS += $(shell $(PYTHON_PREFIX) -m pybind11 --includes)

LIB_SUFFIX ?= $(shell $(PYTHON_PREFIX)-config --extension-suffix)

