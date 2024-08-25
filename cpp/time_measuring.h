/**
 * @file time_measuring.h
 * @brief Functions for measuring the execution time of algorithms.
 *
 * This header file provides functions to measure and record the execution times of various 
 * algorithms implemented in the project. It includes utility functions to reset the state 
 * of the system, measure execution times across different benchmarks, and save the results 
 * to a CSV file.
 *
 * The core functionalities include:
 * - Resetting the state of the rules and facts base.
 * - Measuring execution times for both individual and multiple algorithms across benchmarks.
 * - Saving the measured execution times to a CSV file for further analysis.
 */
#ifndef TIME_MEASURING_H
#define TIME_MEASURING_H

#include <vector>
#include <memory>
#include <utility>
#include <string>
#include "classes.h"


/**
 * @brief Resets the state of the rules, facts base, and question.
 *
 * This function resets the internal state of all rules, facts, and the question to ensure a clean state
 * before each execution of the algorithms. This includes clearing any computed results, flags, or temporary
 * data stored in the objects.
 *
 * @param rules A vector of shared pointers to the rules that need to be reset.
 * @param facts_base A vector of shared pointers to the variables representing the facts base.
 * @param question A shared pointer to the variable representing the question.
 */
void reset_state(const std::vector<std::shared_ptr<Rule>>& rules, const std::vector<std::shared_ptr<Variable>>& facts_base, const std::shared_ptr<Variable>& question);


/**
 * @brief Measures the execution time of a specified algorithm on benchmarks of increasing size.
 *
 * This function measures the execution time of either the forward or backward algorithm on benchmarks
 * with increasing sizes. It averages the execution time over a specified number of repetitions for accuracy.
 *
 * @param alg A string specifying the algorithm to measure ("forward" or "backward").
 * @param num_bench An integer representing the benchmark number to use.
 * @param k An integer representing the parameter k for the benchmark.
 * @param sizes A vector of integers representing the sizes of the benchmarks to test.
 * @param repeat An integer specifying the number of times to repeat the measurement for averaging.
 * @param oriented A boolean indicating if the benchmarks should be oriented (relevant to certain benchmarks).
 * @return A vector of pairs where each pair consists of a benchmark size and the corresponding average execution time.
 */
std::vector<std::pair<int, double>> measure_execution_time(std::string alg, int num_bench, int k, const std::vector<int>& sizes, int repeat);


/**
 * @brief Measures the execution time of both forward and backward algorithms on benchmarks of increasing size.
 *
 * This function measures the execution time of both the forward and backward algorithms on benchmarks
 * with increasing sizes. It averages the execution time over a specified number of repetitions for accuracy
 * and returns the results for both algorithms.
 *
 * @param num_bench An integer representing the benchmark number to use.
 * @param k An integer representing the parameter k for the benchmark.
 * @param sizes A vector of integers representing the sizes of the benchmarks to test.
 * @param repeat An integer specifying the number of times to repeat the measurement for averaging.
 * @return A pair of vectors where each vector consists of pairs of benchmark size and the corresponding average execution time, 
 *         one for the forward algorithm and one for the backward algorithm.
 */
std::pair<std::vector<std::pair<int, double>>, std::vector<std::pair<int, double>>>
measure_both_execution_time(int num_bench, int k, const std::vector<int>& sizes, int repeat);

/**
 * @brief Measures preprocessing time for both forward and backward algorithms on benchmarks of increasing size.
 *
 * This function measures the preprocessing time for both the forward and backward algorithms across various benchmark sizes.
 * The function repeats the measurements a specified number of times to ensure accuracy and returns the average preprocessing
 * times for both algorithms.
 *
 * @param num_bench An integer representing the benchmark number to use.
 * @param k An integer representing the parameter k for the benchmark.
 * @param sizes A vector of integers representing the sizes of the benchmarks to test.
 * @param repeat An integer specifying the number of times to repeat the measurement for averaging.
 * @return A pair of vectors where each vector consists of pairs of benchmark size and the corresponding average preprocessing time, 
 *         one for the forward algorithm and one for the backward algorithm.
 */
std::pair<std::vector<std::pair<int, double>>, std::vector<std::pair<int, double>>>
measure_both_preprocessing_time(int num_bench, int k, const std::vector<int>& sizes, int repeat);


/**
 * @brief Generates a list of sizes for benchmarking.
 *
 * This function generates a vector of integers representing sizes from a specified start to end, 
 * with a given step size. The sizes represent the sizes of the benchmarks to be tested.
 *
 * @param start The starting size for the benchmarks.
 * @param end The ending size for the benchmarks.
 * @param step The increment size between each benchmark size.
 * @return A vector of integers representing the sizes to be used for benchmarking.
 */
std::vector<int> generate_sizes(int start, int end, int step);


/**
 * @brief Saves execution times to a CSV file.
 *
 * This function takes a vector of pairs, where each pair consists of a benchmark size and the corresponding
 * execution time, and saves this data to a CSV file for later analysis.
 *
 * @param execution_times A vector of pairs representing benchmark sizes and execution times.
 * @param filename The name of the CSV file to save the data to.
 */
void save_execution_times_to_csv(const std::vector<std::pair<int, double>>& execution_times, const std::string& filename);

#endif // TIME_MEASURING_H
