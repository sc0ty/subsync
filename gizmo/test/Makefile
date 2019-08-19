####################################
### default global configuration ###
####################################

TARGET ?= tests

CXXFLAGS += \
			-O0 \
			-g \
			-Wall \
			-Wextra \
			-pedantic \
			-fPIC \
			-std=c++14 \
			-fvisibility=hidden \
			-I.. \


######################
### artifact files ###
######################

SOURCES = \
		  core.cpp \
		  utf8.cpp \
		  ssa.cpp \
		  line.cpp \
		  linefinder.cpp \
		  ../text/utf8.cpp \
		  ../text/ssa.cpp \
		  ../math/point.cpp \
		  ../math/line.cpp \
		  ../math/linefinder.cpp \

HEADERS = \
		  catch.hpp \
		  math.h \
		  ../text/utf8.h \
		  ../text/ssa.h \
		  ../math/point.h \
		  ../math/line.h \
		  ../math/linefinder.h \

OBJDIR = obj/test

OBJECTS = $(addprefix $(OBJDIR)/,$(SOURCES:.cpp=.o))


#####################
### build recipes ###
#####################

all: test


test: $(TARGET) | .FORCE
	./$(TARGET)


clean:
	$(RM) $(OBJECTS)
	$(RM) $(TARGET)


$(OBJECTS): $(OBJDIR)/%.o: %.cpp $(HEADERS)
	@mkdir -p $(dir $@)
	$(CXX) -c -o $@ $< $(CXXFLAGS)


$(TARGET): $(OBJECTS)
	$(CXX) -o $@ $^ $(LDFLAGS)


.PHONY: all test clean
.PHONY: .FORCE
