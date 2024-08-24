/**
 * @file forward.h
 * @brief Functions for implementing the forward algorithm.
 *
 * This header file provides the declarations for functions that implement the forward algorithm,
 * a method used in rule-based systems to infer conclusions from a set of facts and rules. The forward 
 * algorithm works by iteratively applying rules to known facts to infer new facts until a 
 * desired conclusion is reached or no more inferences can be made.
 *
 * The file includes functionalities for:
 * - Preprocessing the facts and rules, both with and without step-by-step visualization.
 * - Executing the forward algorithm using either a vector or a deque for the facts base.
 * - Providing step-by-step output for debugging and understanding the algorithm's execution.
 *
 * The forward algorithm is commonly used in expert systems, rule-based reasoning, and other
 * artificial intelligence applications where a set of rules is used to derive conclusions from known facts.
 */


#ifndef FORWARD_H
#define FORWARD_H

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <deque>
#include "classes.h"

/**
 * @brief Preprocesses the facts base and rules, returning a queue instead of a vector.
 *
 * This function prepares the data and returns a deque instead of a vector, which may be more efficient for certain operations
 * within the forward algorithm.
 *
 * @param facts_base The vector of shared pointers to Variable objects representing the facts.
 * @param rules The vector of shared pointers to Rule objects representing the rules.
 * @return A deque of shared pointers to Variable objects representing the preprocessed facts.
 */
std::deque<std::shared_ptr<Variable>> forward_pre_processing_queue(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules);

/**
 * @brief Executes the forward algorithm using a queue-based facts base.
 *
 * This function uses a deque instead of a vector for the facts base, which may improve performance in certain scenarios.
 * It checks if the given question can be inferred from the facts base.
 *
 * @param facts_base The deque of shared pointers to Variable objects representing the facts.
 * @param question The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */
bool forward_algorithm_queue(std::deque<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question);

/**
 * @brief Executes the queue-based forward algorithm with step-by-step output.
 *
 * This function is similar to forward_algorithm_queue but includes additional output to visualize the steps of the algorithm.
 * It is useful for debugging or understanding the process.
 *
 * @param facts_base The deque of shared pointers to Variable objects representing the facts.
 * @param question The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */
bool forward_algorithm_queue_steps(std::deque<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question);

/**
 * @brief Preprocesses the facts base and rules before executing the forward algorithm.
 *
 * This function prepares the data by setting up necessary links between the rules and the facts.
 * It is essential to call this function before running the forward algorithm.
 *
 * @param facts_base The vector of shared pointers to Variable objects representing the facts.
 * @param rules The vector of shared pointers to Rule objects representing the rules.
 */
void pre_processing(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules);

/**
 * @brief Executes the forward algorithm to determine if the question can be inferred from the facts base.
 *
 * This function performs the same operations as forward_algorithm_queue but uses a vector instead of a deque for the facts base.
 *
 * @param facts_base The vector of shared pointers to Variable objects representing the facts.
 * @param question The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */
bool forward_algorithm(std::vector<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question);


/**
 * @brief Executes the forward algorithm with step-by-step output.
 *
 * This function is similar to forward_algorithm but includes additional output to visualize the steps of the algorithm.
 * It uses a vector for the facts base.
 *
 * @param facts_base The vector of shared pointers to Variable objects representing the facts.
 * @param question The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */
bool forward_algorithm_steps(std::vector<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question);

/**
 * @brief Preprocesses the facts base and rules with step-by-step output.
 *
 * This function prepares the data by setting up necessary links between the rules and the facts.
 * It includes additional output to visualize the preprocessing steps.
 *
 * @param facts_base The vector of shared pointers to Variable objects representing the facts.
 * @param rules The vector of shared pointers to Rule objects representing the rules.
 */
void pre_processing_steps(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules);

#endif // FORWARD_H
