############################################
### load platform specific configuration ###
############################################

ifndef CFG
	CFG = config.mk
	ifeq (,$(wildcard $(CFG)))
$(info $(CFG) file not found, using auto configuration)
$(info )
		CFG = config/auto.mk
	endif
endif

include $(CFG)


#####################################
### default targets configuration ###
#####################################

CXXFLAGS_REL ?= -O3 \
				-g \
				-fomit-frame-pointer \
				-fexpensive-optimizations \
				-DNDEBUG \

CXXFLAGS_DBG ?= -O0 \
				-g \

CXXFLAGS_PROF ?= -O3 \
				 -pg \
				 -fexpensive-optimizations \
				 -DNDEBUG \


####################################
### default global configuration ###
####################################
LIB_SUFFIX ?= .so
PREFIX ?= /usr/local
TARGET ?= ../subsync/gizmo$(LIB_SUFFIX)


CXXFLAGS += \
			-Wall \
			-Wextra \
			-pedantic \
			-fPIC \
			-std=c++14 \
			-fvisibility=hidden \
			-I. \

LDFLAGS += \
		   -Wl,--as-needed \


######################
### artifact files ###
######################

SOURCES = \
		  extractor.cpp \
		  correlator.cpp \
		  media/demux.cpp \
		  media/stream.cpp \
		  media/audiodec.cpp \
		  media/resampler.cpp \
		  media/subdec.cpp \
		  media/speechrec.cpp \
		  text/translator.cpp \
		  text/dictionary.cpp \
		  text/words.cpp \
		  text/utf8.cpp \
		  text/wordsqueue.cpp \
		  math/point.cpp \
		  math/line.cpp \
		  math/linefinder.cpp \
		  general/exception.cpp \
		  general/logger.cpp \
		  general/thread.cpp \
		  python/wrapper.cpp \
		  python/general.cpp \
		  python/extractor.cpp \
		  python/media.cpp \
		  python/stream.cpp \
		  python/correlator.cpp \
		  python/translator.cpp \

OBJECTS = $(SOURCES:.cpp=.o)

DEPENDS = $(SOURCES:.cpp=.d)


#####################
### build recipes ###
#####################

all: rel

rel:  CXXFLAGS += $(CXXFLAGS_REL)
rel:  LDFLAGS  += $(LDFLAGS_REL)
rel: $(TARGET)
	$(info RELEASE target done)

dbg:  CXXFLAGS += $(CXXFLAGS_DBG)
dbg:  LDFLAGS  += $(LDFLAGS_DBG)
dbg: $(TARGET)
	$(info DEBUG target done)

prof: CXXFLAGS += $(CXXFLAGS_PROF)
prof: LDFLAGS  += $(LDFLAGS_PROF)
prof: $(TARGET)
	$(info PROFILE target done)

clean:
	$(RM) $(OBJECTS)
	$(RM) $(DEPENDS)
	$(RM) $(TARGET)


-include $(DEPENDS)

$(OBJECTS): %.o: %.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)
	$(CXX) -MM $(CXXFLAGS) $*.cpp -MF $*.d -MQ $@


$(TARGET): $(OBJECTS)
	$(CXX) -shared -o $@ $^ $(LDFLAGS)


ycm.flags: .FORCE
	@echo "$(CXXFLAGS) $(LDFLAGS)" > $@

-include test/test.mk

.PHONY: all build clean
.PHONY: rel dbg prof
.PHONY: .FORCE
