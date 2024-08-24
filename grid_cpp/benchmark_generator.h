/**
 * @file benchmark_generator.h
 * @brief Contains functions for generating benchmarks in string format.
 * 
 * This file includes functions that generate different types of benchmarks 
 * based on the specified parameters. It includes rule generation, 
 * facts base generation, and question generation for different benchmarks.
 */


#ifndef BENCHMARK_GENERATOR_H
#define BENCHMARK_GENERATOR_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <memory>
#include <cstdlib>
#include <any>


/**
 * @brief Generates rules for Benchmark 1.
 *
 * This function generates a set of rules for Benchmark 1. It creates `n` rules
 * for each `k`, where each rule connects a variable `Pj.i` to `P(j+1).i`.
 * 
 * @param k Number of sequences (or columns) to generate.
 * @param n Number of steps (or rows) in each sequence.
 * @param variables_base Vector to store all the variables used in the benchmark.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark1(int k, int n, std::vector<std::string>& variables_base);

/**
 * @brief Generates rules for Benchmark 2.
 *
 * This function generates a set of rules for Benchmark 2. Rules alternate between
 * even and odd indices, creating connections based on the index parity.
 * 
 * @param k Number of sequences (or columns) to generate.
 * @param n Number of steps (or rows) in each sequence.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark2(int k, int n);

/**
 * @brief Generates rules for Benchmark 3.
 *
 * This function generates a complete graph of rules where each variable can potentially
 * be connected to every other variable. The `oriented` flag controls whether the rules
 * are directed or undirected.
 * 
 * @param k Number of variables.
 * @param oriented If true, generates directed rules; otherwise, generates undirected rules.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark3(int k, bool oriented);

/**
 * @brief Generates rules for the worst-case scenario in Benchmark 3.
 *
 * This function generates rules that represent the worst-case scenario for Benchmark 3,
 * where the rules are ordered in a way that makes the problem harder to solve.
 * 
 * @param k Number of variables.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark3_worst(int k);

/**
 * @brief Generates rules for Benchmark 4.
 *
 * This function generates a set of rules for Benchmark 4. It creates rules where
 * each variable depends on a conjunction of several other variables.
 * 
 * @param k Number of variables.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark4(int k);

/**
 * @brief Generates rules for Benchmark 5.
 *
 * This function generates a hierarchical set of rules for Benchmark 5, where the
 * number of rules grows exponentially with the depth `n`.
 * 
 * @param k Branching factor, controlling how many consequents each antecedent has.
 * @param n Depth of the hierarchy.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark5(int k, int n);

/**
 * @brief Generates rules for the specified benchmark.
 *
 * This function acts as a dispatcher, generating rules for the specified benchmark
 * based on the `num_bench` parameter.
 * 
 * @param num_bench The benchmark number to generate rules for.
 * @param k Number of variables or sequences.
 * @param n Number of steps or depth.
 * @param variable_base Vector to store all the variables used in the benchmark.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark(int num_bench, int k, int n, std::vector<std::string>& variable_base);

/**
 * @brief Generates rules for the worst-case scenario of the specified benchmark.
 *
 * This function generates the worst-case scenario rules for the specified benchmark.
 * 
 * @param num_bench The benchmark number to generate rules for.
 * @param k Number of variables or sequences.
 * @param n Number of steps or depth.
 * @param variable_base Vector to store all the variables used in the benchmark.
 * @return A vector of rules, where each rule is represented as a vector of strings.
 */
std::vector<std::vector<std::string>> generate_rules_benchmark_worst(int num_bench, int k, int n);

/**
 * @brief Generates a facts base for the specified benchmark.
 *
 * This function generates the initial facts base for the specified benchmark
 * using the generated rules.
 * 
 * @param num_bench The benchmark number to generate the facts base for.
 * @param rules The generated rules for the benchmark.
 * @param n Number of steps or depth.
 * @return A vector of facts represented as strings.
 */
std::vector<std::string> generate_fb_benchmark(int num_bench, const std::vector<std::vector<std::string>>& rules, int n);

/**
 * @brief Generates a question from a list of possible questions.
 *
 * This function selects a random question from a list of questions. If `cheat`
 * is set to true, the last question in the list is chosen.
 * 
 * @param listOfQuestions The list of potential questions.
 * @param cheat If true, the last question in the list is selected.
 * @return The selected question as a string.
 */
std::string generate_question(const std::vector<std::string>& listOfQuestions, bool cheat = false);

/**
 * @brief Generates a question for the specified benchmark.
 *
 * This function generates a question for the specified benchmark based on
 * the benchmark number and parameters `k` and `n`.
 * 
 * @param num_bench The benchmark number to generate the question for.
 * @param k Number of variables or sequences.
 * @param n Number of steps or depth.
 * @return The generated question as a string.
 */
std::string generate_question1(int num_bench, int k, int n);

/**
 * @brief Generates a complete benchmark with rules, facts base, and question.
 *
 * This function generates the rules, facts base, and question for the specified
 * benchmark and returns them in a map.
 * 
 * @param num_bench The benchmark number to generate.
 * @param k Number of variables or sequences.
 * @param n Number of steps or depth.
 * @return A map containing the generated rules, facts base, and question.
 */
std::unordered_map<std::string, std::shared_ptr<std::any>> generate_benchmark(int num_bench, int k, int n);

/**
 * @brief Generates a complete worst-case scenario benchmark.
 *
 * This function generates the rules, facts base, and question for the specified
 * worst-case scenario benchmark and returns them in a map.
 * 
 * @param num_bench The benchmark number to generate.
 * @param k Number of variables or sequences.
 * @param n Number of steps or depth.
 * @return A map containing the generated rules, facts base, and question.
 */
std::unordered_map<std::string, std::shared_ptr<std::any>> generate_benchmark_worst(int num_bench, int k, int n);

#endif // BENCHMARK_GENERATOR_H
