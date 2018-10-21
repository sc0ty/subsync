####################################
### default global configuration ###
####################################

TEST_DIR = test

TEST_TARGET = $(TEST_DIR)/tests


######################
### artifact files ###
######################

TEST_SOURCES = \
			   $(TEST_DIR)/core.cpp \
			   $(TEST_DIR)/utf8.cpp \

TEST_OBJECTS = $(TEST_SOURCES:.cpp=.o)

TEST_DEPENDS = $(TEST_SOURCES:.cpp=.d)

TESTEE_OBJECTS = \
				 text/utf8.o


#####################
### build recipes ###
#####################

test:  CXXFLAGS += $(CXXFLAGS_DBG)
test:  LDFLAGS  += $(LDFLAGS_DBG)
test: $(TEST_TARGET) | .FORCE
	$(TEST_TARGET)

test-clean:
	$(RM) $(TEST_OBJECTS)
	$(RM) $(TEST_TARGET)

clean: test-clean


-include $(DEPENDS)

$(TEST_OBJECTS): %.o: %.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)
	$(CXX) -MM $(CXXFLAGS) $*.cpp -MF $*.d -MQ $@


$(TEST_TARGET): $(TEST_OBJECTS) $(TESTEE_OBJECTS)
	$(CXX) -o $@ $^ $(LDFLAGS)

.PHONY: test test-clean
.PHONY: .FORCE
