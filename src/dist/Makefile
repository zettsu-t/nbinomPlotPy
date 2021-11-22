DIR_BOOST=/opt/boost
DIR_GTEST=/opt/googletest/googletest
DIR_PYTHON_HEADER=$(shell find /usr/include -type f -name "Python.h" | tail -1 | xargs dirname)

GTEST_SOURCE=$(DIR_GTEST)/src/gtest-all.cc
GTEST_OBJ=$(patsubst %.cc, %.o, $(notdir $(GTEST_SOURCE)))

HEADERS=dist.hpp
SOURCE_PY=dist.cpp
SOURCE_IMPL=dist_impl.cpp
SOURCE_TEST=../../tests/test_dist.cpp

OBJ_PY=dist.o
OBJ_IMPL=dist_impl.o
OBJ_TESTED=tested_dist_impl.o
OBJ_TEST=test_dist.o
OBJS=$(OBJ_PY) $(OBJ_IMPL) $(OBJ_TESTED) $(OBJ_TEST) $(GTEST_OBJ)

TARGET_PY=libnb_plot_streamlit.so
TARGET_TEST=test_dist
TARGETS=$(TARGET_PY) $(TARGET_TEST)

INCLUDE_PYTHON=$(DIR_PYTHON_HEADER)
INCLUDE_BOOST=$(DIR_BOOST)/include
INCLUDE_GTEST=$(DIR_GTEST)/include
INCLUDES=$(addprefix -I, $(INCLUDE_PYTHON) $(INCLUDE_BOOST))

CXX=g++
LD=g++
OPT=-O2

CPPFLAGS=-std=gnu++14 -Wall
CPPFLAGS_PY=$(CPPFLAGS) -DPIC -shared -fPIC
CPPFLAGS_TEST=$(CPPFLAGS)
LIBPATH=$(addprefix -L, $(DIR_BOOST)/lib)
LDFLAGS_PY=-DPIC -shared -fPIC
LDFLAGS_TEST=
LIBS_PY=-lboost_python
LIBS_TEST=-lpthread -lboost_python

.PHONY: all test clean

all: $(TARGETS)

test: $(TARGETS)
	./$(TARGET_TEST)

$(TARGET_PY): $(OBJ_PY) $(OBJ_IMPL)
	$(LD) $(LIBPATH) -o $@ $^ $(LDFLAGS_PY) $(LIBS_PY)

$(TARGET_TEST): $(OBJ_TESTED) $(OBJ_TEST) $(GTEST_OBJ)
	$(LD) $(LIBPATH) -o $@ $^ $(LDFLAGS_TEST) $(LIBS_TEST)

$(OBJ_PY): $(SOURCE_PY) $(HEADERS)
	$(CXX) $(INCLUDES) $(OPT) $(CPPFLAGS_PY) -o $@ -c $<

$(OBJ_IMPL): $(SOURCE_IMPL) $(HEADERS)
	$(CXX) $(INCLUDES) $(OPT) $(CPPFLAGS_PY) -o $@ -c $<

$(OBJ_TESTED): $(SOURCE_IMPL) $(HEADERS)
	$(CXX) $(INCLUDES) $(CPPFLAGS_TEST) -o $@ -c $<

$(OBJ_TEST): $(SOURCE_TEST) $(HEADERS)
	$(CXX) $(INCLUDES) -I. -I$(INCLUDE_GTEST) $(CPPFLAGS_TEST) -o $@ -c $<

$(GTEST_OBJ): $(GTEST_SOURCE)
	$(CXX) $(INCLUDES) -I$(DIR_GTEST) -I$(INCLUDE_GTEST) $(CPPFLAGS_TEST) -o $@ -c $<

clean:
	rm -f $(TARGETS) $(OBJS)

show:
	$(foreach v, $(.VARIABLES), $(info $(v) = $($(v))))
