#ifndef TIME_PREPROCESSING_H
#define TIME_PREPROCESSING_H


/*
This file provides functions to measure execution times of the algorithms implemented.

*/
#include <vector>
#include <memory>
#include <utility>
#include <string>
#include "classes.h"


// Function to reset the state of the rules and facts_base
void reset_state(const std::vector<std::shared_ptr<Rule>>& rules, const std::vector<std::shared_ptr<Variable>>& facts_base, const std::shared_ptr<Variable>& question);

std::pair< std::vector<std::pair<int, double>>,std::vector<std::pair<int, double>> > measure_both_preprocessing_time(int num_bench, int k, const std::vector<int>& sizes, int repeat);

// Function to generate a list of sizes for benchmarking
std::vector<int> generate_sizes(int start, int end, int step);

// Function to save execution times to a CSV file
void save_execution_times_to_csv(const std::vector<std::pair<int, double>>& execution_times, const std::string& filename);

#endif // TIME_MEASURING_H
