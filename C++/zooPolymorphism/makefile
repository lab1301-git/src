############################################################################
# 'A Generic Makefile for Building Multiple main() Targets in $PWD'
############################################################################
#
PRG_SUFFIX_FLAG := 0
#
CC := g++
LIBS = -lpthread -lncurses
LDFLAGS := -L -std=c++17 -g -Wall
LDFLAGS := -g $(LIBS)
CFLAGS_INC := -I.
CFLAGS := -std=c++17 -g $(CFLAGS_INC) -Wall
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
$(info $$  SRCS:    ${SRCS})
$(info $$  CC:      ${CC})
$(info $$  CFLAGS:  ${CFLAGS})
$(info $$  LIBS:    ${LIBS})
$(info $$  LDFLAGS: ${LDFLAGS})
$(info $$  OBJS:    ${OBJS})
$(info $$  BINS:    ${BINS})
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
	$(info $$ *** make called with no args ***)
	$(CC) $(CFLAGS) -c $< -o $@

%.d: %.cpp
	$(CC) $(CFLAGS_INC) -MM $< > $@

all : $(BINS)

$(BINS): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LIBS) -o $@

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
