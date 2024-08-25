/**
 * @file backward.h
 * @brief Functions for implementing the backward chaining algorithm.
 *
 * This header file provides the declarations for functions that implement the backward chaining algorithm,
 * a method used in rule-based systems to infer the truth of a hypothesis (or query) by working backward from 
 * the goal (the query) to the known facts. The backward chaining algorithm is typically used in logic 
 * programming and expert systems.
 *
 * The file includes functionalities for:
 * - Preprocessing the rules and facts base before running the backward algorithm.
 * - Executing the backward chaining algorithm with both standard and step-by-step output.
 * - Managing the execution state during the backward reasoning process.
 * - Supporting operations like OR (checking if any rule makes a variable true) and AND (checking if all 
 *   conditions of a rule are satisfied) as part of the backward reasoning.
 *
 * The backward chaining algorithm is used in applications where you need to prove a hypothesis or derive 
 * a specific goal based on a set of rules and known facts.
 */


#ifndef BACKWARD_H
#define BACKWARD_H

#include <limits>
#include <vector>
#include <memory>
#include "classes.h"
#include <variant>

/**
 * @brief Structure to maintain the state during the execution of the backward algorithm.
 * 
 * The structure keeps track of the current execution state, including the counter,
 * the root variable, and the list of variables currently being processed.
 */
struct ExecutionState {
    int counter = 0;
    int root = std::numeric_limits<int>::max();
    std::vector<std::shared_ptr<Variable>> on_list;
};

/**
 * @brief Preprocesses the rules and facts base before running the backward algorithm.
 *
 * This function prepares the data, setting up necessary links between the rules and the facts base.
 *
 * @param rules The vector of shared pointers to Rule objects representing the rules.
 * @param facts_base The vector of shared pointers to Variable objects representing the facts base.
 */
void backward_pre_processing(std::vector<std::shared_ptr<Rule>>& rules, std::vector<std::shared_ptr<Variable>>& facts_base);

/**
 * @brief Launches the backward algorithm.
 *
 * This function initiates the backward reasoning process by calling the OR function on the question.
 * It aims to determine whether the given question can be inferred from the facts base.
 *
 * @param Q The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */

bool backward_algorithm(std::shared_ptr<Variable>& Q);

/**
 * @brief Checks if a variable is true by performing an OR operation on the rules where it is a consequence.
 *
 * This function verifies whether a variable can be satisfied by checking if the body of any rule leading to it is satisfied.
 * The OR operation is necessary because satisfying any rule with the variable as a consequence makes the variable true.
 *
 * @param P The shared pointer to the Variable object being checked.
 * @param state The current execution state.
 */
void OR(std::shared_ptr<Variable>& P, ExecutionState& state);

/**
 * @brief Checks if the body of a given rule is satisfied (AND operation).
 *
 * This function checks whether all the variables in the body of a rule are satisfied by calling the OR function on each of them.
 * The AND operation is needed because all variables in the body must be satisfied for the rule to hold.
 *
 * @param R The shared pointer to the Rule object representing the rule.
 * @param state The current execution state.
 * @return A variant that either contains a boolean result or a vector of pointers to satisfied variables.
 */
std::variant<bool, std::vector<std::shared_ptr<Variable>>> AND(std::shared_ptr<Rule>& R, ExecutionState& state);



/**
 * @brief Processes the inverse deduction when a consequence is deduced.
 *
 * This function attempts to deduce additional variables based on the newly deduced consequence.
 *
 * @param P The shared pointer to the Variable object that has been deduced.
 */
void INVERSE(std::shared_ptr<Variable>& P, ExecutionState& state);

/**
 * @brief Assigns the current state as false when no further deduction is possible.
 *
 * This function updates the execution state, marking it as false when no rules can be satisfied or when a deduction fails.
 *
 * @param state The current execution state.
 */
void assing_false(ExecutionState& state);

/**
 * @brief Executes the backward algorithm with detailed step-by-step output for debugging or educational purposes.
 *
 * This function is similar to backward_algorithm but provides additional output to visualize the steps of the algorithm.
 *
 * @param Q The shared pointer to the Variable object representing the question.
 * @return True if the question can be inferred; false otherwise.
 */
bool backward_algorithm_steps(std::shared_ptr<Variable>& Q);

/**
 * @brief Checks if a variable is true with step-by-step output (OR operation).
 *
 * This function is similar to OR but includes detailed output for each step, which is useful for understanding the process.
 *
 * @param P The shared pointer to the Variable object being checked.
 * @param state The current execution state.
 */
void OR_steps(std::shared_ptr<Variable>& P, ExecutionState& state);

/**
 * @brief Checks if the body of a given rule is satisfied with step-by-step output (AND operation).
 *
 * This function is similar to AND but provides detailed output for each step, useful for understanding the process.
 *
 * @param R The shared pointer to the Rule object representing the rule.
 * @param state The current execution state.
 * @return A variant that either contains a boolean result or a vector of pointers to satisfied variables.
 */
std::variant<bool, std::vector<std::shared_ptr<Variable>>> AND_steps(std::shared_ptr<Rule>& R, ExecutionState& state);

/**
 * @brief Processes the inverse deduction with step-by-step output when a consequence is deduced.
 *
 * This function is similar to INVERSE but includes detailed output for each step, useful for understanding the process.
 *
 * @param P The shared pointer to the Variable object that has been deduced.
 */
void INVERSE_steps(std::shared_ptr<Variable>& P,ExecutionState& state);

/**
 * @brief Assigns the current state as false with step-by-step output.
 *
 * This function is similar to assing_false but provides detailed output for each step, useful for understanding the process.
 *
 * @param state The current execution state.
 */
void assing_false_steps(ExecutionState& state);

#endif // BACKWARD_H
