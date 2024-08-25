/**
 * @file input_parser.h
 * @brief Functions to parse string-based input data into structured objects.
 * 
 * This file contains functions that convert string representations of rules, 
 * facts base, and questions into structured objects like Variable and Rule.
 * 
 * The create_set function takes input data in an unordered_map format and 
 * returns a structured representation of the benchmark.
 * 
 * Other functions handle the parsing of individual rules, antecedents, 
 * consequents, facts, and questions from their string representations 
 * into objects that can be used in the reasoning algorithms.
 */


#ifndef INPUT_PARSER_H
#define INPUT_PARSER_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <any>
#include "classes.h"

/**
 * @brief Creates a set of parsed rules, facts base, and question from the given data.
 *
 * This function takes in a data structure that includes the rules, facts base, and question
 * in string format, parses this data, and converts it into a more structured format
 * (e.g., Rule and Variable objects).
 *
 * The input data should be an unordered_map structured as follows:
 * - "rules": A vector of vectors of strings, where each inner vector represents a rule.
 * - "facts base": A vector of strings, where each string represents a fact.
 * - "question": A single string representing the question.
 *
 * Example structure:
 * @code
 * std::unordered_map<std::string, std::shared_ptr<std::any>> data;
 * data["rules"] = std::make_shared<std::any>(std::vector<std::vector<std::string>>{
 *     {"A", "B"}, {"B", "C"}});
 * data["facts base"] = std::make_shared<std::any>(std::vector<std::string>{"A"});
 * data["question"] = std::make_shared<std::any>(std::string{"C"});
 * @endcode
 *
 * @param data An unordered_map containing the rules, facts base, and question in string format.
 * @return An unordered_map containing the parsed rules, facts base, and question as objects.
 */
std::unordered_map<std::string, std::shared_ptr<std::any>> create_set(const std::unordered_map<std::string, std::shared_ptr<std::any>>& data);


/**
 * @brief Converts a vector of strings representing a rule into a Rule object.
 *
 * This function converts a vector of strings into a Rule object. The vector typically contains
 * the antecedents and consequent of a rule.
 *
 * @param listRule A vector of strings representing the rule.
 * @param variables A map to keep track of the created Variable objects.
 * @return A shared_ptr to the created Rule object.
 */
std::shared_ptr<Rule> vector_to_rule(const std::vector<std::string>& listRule, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables);


/**
 * @brief Creates a list of shared_ptr to Variable objects from a vector of strings.
 *
 * This function creates a list of antecedent objects (as shared_ptr) from a list of strings.
 *
 * @param list A vector of strings representing the antecedents.
 * @param variables A map to keep track of the created Variable objects.
 * @return A vector of shared_ptr to the created Variable objects.
 */
std::vector<std::shared_ptr<Variable>> create_ant(const std::vector<std::string>& list, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables);


/**
 * @brief Creates a shared_ptr to a Variable object representing the consequent.
 *
 * This function creates a consequent object (as shared_ptr) from a string.
 *
 * @param var A string representing the consequent.
 * @param variables A map to keep track of the created Variable objects.
 * @return A shared_ptr to the created Variable object.
 */
std::shared_ptr<Variable> create_csq(const std::string& var, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables);

/**
 * @brief Creates a shared_ptr to a Variable object representing the question.
 *
 * This function creates a question object (as shared_ptr) from a string.
 *
 * @param question A string representing the question.
 * @param variables A map to keep track of the created Variable objects.
 * @return A shared_ptr to the created Variable object.
 */
std::shared_ptr<Variable> create_question(const std::string& question, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables);

/**
 * @brief Creates a list of shared_ptr to Variable objects representing the facts base.
 *
 * This function creates the facts base from a list of strings. Each string represents a fact.
 *
 * @param list A vector of strings representing the facts base.
 * @param variables A map to keep track of the created Variable objects.
 * @return A vector of shared_ptr to the created Variable objects.
 */
std::vector<std::shared_ptr<Variable>> create_fb(const std::vector<std::string>& list, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables);

/**
 * @brief Parses a string using a given connector.
 *
 * This function splits a string using the specified connector and returns a vector
 * of substrings.
 *
 * @param string The string to be parsed.
 * @param connector The connector used to split the string.
 * @return A vector of strings obtained by splitting the input string.
 */
std::vector<std::string> parse_connector(std::string string, std::string connector);

/**
 * @brief Parses a rule represented as a vector of strings.
 *
 * This function takes a vector of strings representing a rule and splits it into
 * antecedents and consequent.
 *
 * @param rule A vector of strings representing the rule.
 * @return An unordered_map containing the antecedents and consequent of the rule.
 */
std::unordered_map<std::string, std::any> parse_rule(std::vector<std::string> rule);

#endif // INPUT_PARSER_H
