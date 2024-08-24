# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++20 -Wall -Wextra -O2

# Source files
SOURCES_TIME_MEASURING = time_measuring.cpp classes.cpp benchmark_generator.cpp input_parser.cpp forward.cpp backward.cpp
SOURCES_TIME_PREPROCESSING = time_preprocessing.cpp classes.cpp benchmark_generator.cpp input_parser.cpp forward.cpp backward.cpp
SOURCES_TESTS = tests.cpp classes.cpp benchmark_generator.cpp input_parser.cpp forward.cpp backward.cpp json_parser.cpp
SOURCES_SIZE_MEASURING = size_measuring.cpp classes.cpp


# Executable names
TARGET_TIME_MEASURING = time_measuring_exec
TARGET_TIME_PREPROCESSING = time_preprocessing_exec
TARGET_TESTS = tests_exec
TARGET_SIZE_MEASURING = size_measuring_exec


# Default target
all: $(TARGET_TIME_MEASURING) $(TARGET_TIME_PREPROCESSING) $(TARGET_TESTS)

# Compile time_measuring
$(TARGET_TIME_MEASURING): $(SOURCES_TIME_MEASURING)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile time_preprocessing
$(TARGET_TIME_PREPROCESSING): $(SOURCES_TIME_PREPROCESSING)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile tests
$(TARGET_TESTS): $(SOURCES_TESTS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile size_measuring
$(TARGET_SIZE_MEASURING): $(SOURCES_SIZE_MEASURING)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Clean up generated files
clean:
	rm -f $(TARGET_TIME_MEASURING) $(TARGET_TIME_PREPROCESSING) $(TARGET_TESTS) $(TARGET_SIZE_MEASURING)

# Execute time_measuring with arguments
run_time_measuring: $(TARGET_TIME_MEASURING)
	./$(TARGET_TIME_MEASURING) $(num_bench) $(k) $(end) $(step) $(rep) $(algorithm)

# Execute time_preprocessing with arguments
run_time_preprocessing: $(TARGET_TIME_PREPROCESSING)
	./$(TARGET_TIME_PREPROCESSING) $(num_bench) $(k) $(end) $(step) $(rep)

# Execute tests
run_tests: $(TARGET_TESTS)
	./$(TARGET_TESTS)

# Execute size_measuring
run_size_measuring: $(TARGET_SIZE_MEASURING)
	./$(TARGET_SIZE_MEASURING)

# Phony targets
.PHONY: all clean run_time_measuring run_time_preprocessing run_tests run_size_measuring
