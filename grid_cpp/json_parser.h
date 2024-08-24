/**
 * @file json_parser.h
 * @brief Functions for parsing rules, facts base, and questions from a JSON file.
 *
 * This header file provides utilities to handle the parsing of rules, facts base, and questions
 * from a JSON-formatted file. It includes functions to extract and clean data such as rules and facts,
 * as well as utilities to trim unwanted whitespace and characters from strings.
 *
 * The core functionalities include:
 * - Trimming leading and trailing whitespace and quotes from strings.
 * - Extracting and parsing the base of rules, facts base, and questions from the JSON content.
 * - Providing a function to parse a JSON file and return a structured representation of the rules, facts, and questions.
 *
 * These functions are essential for converting JSON input into a format that can be used for logic processing 
 * within the application.
 */


#ifndef JSON_PARSER_H
#define JSON_PARSER_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <any>

/**
 * @brief Trims leading and trailing whitespace from a string.
 *
 * This function modifies the input string by removing any leading or trailing whitespace characters.
 *
 * @param str A reference to the string that will be trimmed.
 */
void trimWhitespace(std::string& str);


/**
 * @brief Trims leading and trailing whitespace and quotes from a string.
 *
 * This function removes any leading or trailing spaces, tabs, newline characters, carriage returns,
 * and double quotes from the input string. If the string consists entirely of whitespace or quotes,
 * an empty string is returned.
 *
 * @param str The input string that may contain leading and/or trailing whitespace and quotes.
 * @return A new string with the leading and trailing whitespace and quotes removed. If the input string 
 *         contains only whitespace or quotes, an empty string is returned.
 */
std::string trim_string(const std::string &str);

/**
 * @brief Extracts the base of rules from the JSON content.
 *
 * This function parses the JSON content to extract the base of rules, which is a collection of rules defined 
 * in the JSON structure. The rules are stored in a vector of vectors of strings.
 *
 * @param content A string containing the JSON content to parse.
 * @param rules A reference to a vector of vectors of strings where the extracted rules will be stored.
 */
void extract_rules(const std::string& content, std::vector<std::vector<std::string>>& rules);

/**
 * @brief Extracts the base of facts from the JSON content.
 *
 * This function parses the JSON content to extract the base of facts, which is a collection of initial facts 
 * defined in the JSON structure. The facts are stored in a vector of strings.
 *
 * @param content A string containing the JSON content to parse.
 * @param factsBase A reference to a vector of strings where the extracted facts will be stored.
 */
void extract_facts_base(const std::string& content, std::vector<std::string>& factsBase);

/**
 * @brief Extracts the question from the JSON content.
 *
 * This function parses the JSON content to extract the question, which is the query or conclusion to be evaluated 
 * based on the rules and facts provided in the JSON structure.
 *
 * @param content A string containing the JSON content to parse.
 * @return A string containing the extracted question.
 */
std::string extract_question(const std::string& content);

/**
 * @brief Parses a JSON file and returns a map containing rules, facts, and the question.
 *
 * This function reads and parses a JSON file to extract the base of rules, base of facts, and the question.
 * The extracted data is stored in an unordered map with keys "rules", "facts base", and "question".
 *
 * @param filename A string representing the path to the JSON file to be parsed.
 * @return An unordered map containing shared pointers to the extracted rules, facts base, and question.
 */
std::unordered_map<std::string, std::shared_ptr<std::any>> parse_json(const std::string& filename);

#endif // PARSER_H
