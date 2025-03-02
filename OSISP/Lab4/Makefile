CXX = g++
CXXFLAGS = -Wall -O2 -std=c++11
TARGET = self_recovering_process

all: $(TARGET)

$(TARGET): main.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.cpp

clean:
	rm -f $(TARGET) counter.txt

.PHONY: all clean
