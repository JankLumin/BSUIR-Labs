# Makefile for Low-Level Sector Editor using ncurses (C++17)

CXX      = g++
CXXFLAGS = -Wall -Wextra -O2 -std=c++17
LDFLAGS  = -lncursesw
TARGET   = editor
SRCS     = main.cpp editor.cpp
OBJS     = $(SRCS:.cpp=.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
