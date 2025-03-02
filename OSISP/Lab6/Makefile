CXX := g++
CXXFLAGS := -Wall -Wextra -std=c++17

SRCS := main.cpp functions.cpp
OBJS := $(SRCS:.cpp=.o)
TARGET := traceroute

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
