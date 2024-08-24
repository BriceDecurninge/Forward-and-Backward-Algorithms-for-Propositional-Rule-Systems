#ifndef TESTS_H
#define TESTS_H

#include "classes.h"
#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <stdexcept>



void reset_state(const std::vector<std::shared_ptr<Rule>>& rules, const std::vector<std::shared_ptr<Variable>>& facts_base, const std::shared_ptr<Variable>& question);

/**
 * @brief Runs the specified algorithm(s) and prints the results.
 * 
 * This function can run either the forward, backward, or both algorithms, depending on the specified argument.
 * It prints the results of the algorithm(s) to the console.
 * 
 * @param algorithm A string specifying which algorithm to run ("forward", "backward", or "both").
 * @param facts_base The vector of shared pointers to Variable objects representing the facts base.
 * @param rules The vector of shared pointers to Rule objects representing the rules.
 * @param question The shared pointer to the Variable object representing the question.
 */
void run_test(const std::string& algorithm, std::vector<std::shared_ptr<Variable>> facts_base, std::vector<std::shared_ptr<Rule>> rules, std::shared_ptr<Variable> question);

/**
 * @brief Test function for simple deduction using a single rule.
 * 
 * This test verifies if the system can deduce a conclusion from a simple set of facts and a single rule.
 * 
 * @param algorithm A string specifying which algorithm to run ("forward", "backward", or "both").
 */
void test_simple_deduction1(const std::string& algorithm);


// Additional test functions for various scenarios
void test_simple_deduction2(const std::string& algorithm);
void test_simple_deduction3(const std::string& algorithm);
void test_simple_deduction4(const std::string& algorithm);
void test_simple_deduction5(const std::string& algorithm);
void test_simple_deduction6(const std::string& algorithm);
void test_deduction_with_cycle1(const std::string& algorithm);
void test_deduction_with_cycle2(const std::string& algorithm);
void test_deduction_with_multiple_cycles(const std::string& algorithm);
void test_non_deducible1(const std::string& algorithm);
void test_non_deducible2(const std::string& algorithm);
void test_non_deducible_with_cycle(const std::string& algorithm);

/**
 * @brief Tests the benchmark generation function.
 * 
 * This function tests the generation of benchmark data, printing the generated rules, facts base, and question.
 * 
 * @param num_bench The benchmark number.
 * @param k The parameter k for the benchmark.
 * @param n The size of the benchmark.
 */
void test_generate_benchmark(int num_bench, int k, int n);

/**
 * @brief Tests the benchmark generation and processing functions.
 * 
 * This function tests the entire process from benchmark generation to running the specified algorithm(s).
 * 
 * @param algorithm A string specifying which algorithm to run ("forward", "backward", or "both").
 * @param num_bench The benchmark number.
 * @param k The parameter k for the benchmark.
 * @param n The size of the benchmark.
 */
void test_generate_and_process_benchmark(const std::string& algorithm, int num_bench, int k, int n);

/**
 * @brief Prints the content of a JSON file parsed into internal structures.
 * 
 * This function reads and prints the content of a JSON file, showing the rules, facts base, and question.
 * 
 * @param filename The name of the JSON file to parse and print.
 */
void test_print_json(const std::string& filename);

/**
 * @brief Runs a test using data from a JSON file.
 * 
 * This function runs the specified algorithm(s) on data parsed from a JSON file and prints the results.
 * 
 * @param algorithm A string specifying which algorithm to run ("forward", "backward", or "both").
 * @param filename The name of the JSON file containing the data.
 */
void test_json(const std::string& algorithm, const std::string& filename);

/**
 * @brief Generates a range of sizes for benchmarking.
 * 
 * This function generates a vector of integers representing sizes from start to end, incremented by step.
 * 
 * @param start The starting size.
 * @param end The ending size.
 * @param step The step size.
 * @return A vector of integers representing the generated sizes.
 */
std::vector<int> generate_sizes(int start, int end, int step);

#endif // TESTS_H
