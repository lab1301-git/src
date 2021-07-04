############################################################################
# 'A Generic Makefile for Building Multiple main() Targets in $PWD'
############################################################################
#
PRG_SUFFIX_FLAG := 0
#
CC := g++
LIBS = -lpthread
LDFLAGS := -L -std=c++14 -g -Wall
LDFLAGS := -g -lpthread
CFLAGS_INC := -I.
CFLAGS := -std=c++14 -g $(CFLAGS_INC) -Wall
#
## ==================- NOTHING TO CHANGE BELOW THIS LINE ===================
##
SRCS := $(wildcard *.cpp)
PRGS := $(patsubst %.cpp,%,$(SRCS))
PRG_SUFFIX=.exe
BINS := $(patsubst %,%$(PRG_SUFFIX),$(PRGS))
## OBJS are automagically compiled by make.
OBJS := $(patsubst %,%.o,$(PRGS))
##

# Verbose option, to output compile and link commands
export V := false
export CMD_PREFIX := @
ifeq ($(V),true)
	CMD_PREFIX :=
endif

$(info $$#################################################)
$(info $$  List of source files being compiled are: ${SRCS})
$(info $$#################################################)

##
## For clarity sake we make use of:
.SECONDEXPANSION:
OBJ = $(patsubst %$(PRG_SUFFIX),%.o,$@)
ifeq ($(PRG_SUFFIX_FLAG),0)
	BIN = $(patsubst %$(PRG_SUFFIX),%,$@)
else
	BIN = $@
endif

# When make is called with no args we arrive here
%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

%.d: %.cpp
	$(CC) $(CFLAGS_INC) -MM $< > $@

all : $(BINS)

$(BINS): $(OBJS)
	$(CC) $(CFLAGS) -o $(OBJS) $(LIBS) -o $@

## Compile the executables 
%$(PRG_SUFFIX) : $(OBJS) $(SRCS) 
	$(CC) $(CFLAGS) $(OBJ) $(LDFLAGS) -o $(BIN)

##
## $(OBJS) should be automagically removed right after linking.
##
clean:
ifeq ($(PRG_SUFFIX_FLAG),0)
	$(RM) $(PRGS) $(OBJS)
else
	$(RM) $(BINS) $(OBJS)
endif
##
rebuild: clean all
##
