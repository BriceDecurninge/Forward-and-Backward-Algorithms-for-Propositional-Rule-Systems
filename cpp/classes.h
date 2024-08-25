/**
 * @file classes.h
 * @brief Defines core classes used in the project, including Variable and Rule.
 * 
 * This file contains the declaration of the Variable and Rule classes, 
 * which represent the variables and rules in a propositional logic system.
 * 
 * The Variable class represents a boolean variable with various states and 
 * methods for evaluation and manipulation. 
 * 
 * The Rule class represents a logical implication (antecedents => consequent), 
 * along with methods to manage and manipulate the rule.
 * 
 * Both classes are heavily used across the project in the implementation 
 * of forward and backward reasoning algorithms.
 */


#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <stdexcept>
#include <memory>
#include <any>
#include <optional>

// Forward declarations
class Rule;

// Constant representing the implication connector
const std::string implique = "=>";

// Enum to represent the state of a Variable
enum class VariableState {
    None,   // Uninitialized state
    True,   // Variable is true
    False,  // Variable is false
    ON      // Variable is in the process of being evaluated
};

/**
 * @brief Class representing a variable in propositional logic.
 *
 * The Variable class models a variable in a propositional rule-based system.
 * It holds the variable's state, associated rules, and additional properties used during algorithm execution.
 */
class Variable {
public:
    std::string name;  ///< The name of the variable.
    VariableState value;  ///< The current state of the variable.
    std::vector<std::weak_ptr<Rule>> rules;  ///< The rules where this variable is an antecedent.
    bool used = false;  ///< Indicates whether the variable has been used in the deduction process.
    

    std::vector<std::weak_ptr<Rule>> successors;  ///< The rules where this variable needs to be further evaluated because of a cylce.
    std::optional<int> order = std::nullopt;  ///< Optional order for processing, used for backward algorithm cycle detection.

    /**
     * @brief Constructor for Variable.
     * 
     * Initializes a variable with the given name and state.
     * 
     * @param name The name of the variable.
     * @param value The initial state of the variable (default is VariableState::None).
     */
    Variable(const std::string& name, VariableState value = VariableState::None);

    /**
     * @brief Destructor for Variable.
     * 
     * Cleans up resources used by the Variable instance.
     */
    ~Variable();

    // Methods declarations:
    
    /**
     * @brief Resets the state of the variable to its initial state.
     */
    void reset();

    /**
     * @brief Checks if two variables are equal based on their names.
     * 
     * @param other The variable to compare with.
     * @return True if the variables have the same name, false otherwise.
     */
    bool operator==(const Variable& other) const;

    /**
     * @brief Converts the variable state to a string representation.
     * 
     * @return A string representation of the variable state.
     */
    std::string to_string_aux() const;

    /**
     * @brief Converts the variable to a string representation (alternative method).
     * 
     * @return A string representation of the variable.
     */
    std::string to_string() const;

    /**
     * @brief Assigns a new state to the variable.
     * 
     * @param state The new state to assign (default is VariableState::True).
     */
    inline void assign(VariableState state = VariableState::True);

    /**
     * @brief Checks if the variable's state is true.
     * 
     * @return True if the variable's state is true, false otherwise.
     */
    inline bool is_true() const;

    /**
     * @brief Evaluates the current state of the variable.
     * 
     * @return The current state of the variable.
     */
    inline VariableState evaluate() const;

    /**
     * @brief Marks the variable as used.
     */
    inline void use();

    /**
     * @brief Checks if the variable has been used.
     * 
     * @return True if the variable has been used, false otherwise.
     */
    inline bool is_used() const;

    /**
     * @brief Adds a rule to the list of rules where this variable is an antecedent.
     * 
     * @param rule The rule to add.
     */
    inline void add_rule(std::shared_ptr<Rule> rule);


    /**
     * @brief Adds a rule to the list of successors.
     * 
     * @param successor The rule to add.
     */
    inline void add_successor(std::weak_ptr<Rule> successor);
};

// Inline function implementations

inline void Variable::assign(VariableState state) {
    value = state;
}

inline bool Variable::is_true() const {
    return value == VariableState::True;
}

inline VariableState Variable::evaluate() const {
    return value;
}

inline void Variable::use() {
    used = true;
}

inline bool Variable::is_used() const {
    return used;
}

inline void Variable::add_rule(std::shared_ptr<Rule> rule) {
    rules.push_back(rule);
}


inline void Variable::add_successor(std::weak_ptr<Rule> successor) {
    successors.push_back(successor);
}

/**
 * @brief Class representing a rule in propositional logic.
 *
 * The Rule class models a logical rule, consisting of a set of antecedent variables and a consequent variable.
 */
class Rule {
public:
    std::vector<std::shared_ptr<Variable>> antecedents;  ///< The variables that make up the body of the rule (antecedents).
    const std::string connector = implique;  ///< The logical connector used in the rule (default is "=>").
    
    std::shared_ptr<Variable> consequent;  ///< The variable that is deduced if the antecedents are true (consequent).
    int counter;  ///< The number of antecedents in the body.
    std::vector<std::shared_ptr<Variable>> successors;  ///< Variables that need to be further evaluated because of a cycle.

    /**
     * @brief Constructor for Rule.
     * 
     * Initializes a rule with the given antecedents and consequent.
     * 
     * @param antecedents The list of variables forming the body of the rule.
     * @param consequent The variable that is deduced if the antecedents are true.
     * @param counter The number of antecedents in the body (default is 0).
     */
    Rule(const std::vector<std::shared_ptr<Variable>>& antecedents, const std::shared_ptr<Variable>& consequent, int counter = 0);

    /**
     * @brief Destructor for Rule.
     * 
     * Cleans up resources used by the Rule instance.
     */
    ~Rule();

    // Methods declarations

    /**
     * @brief Converts the rule to a string representation.
     * 
     * @return A string representation of the rule.
     */
    std::string to_string() const;

    /**
     * @brief Adds a variable to the list of successors.
     * 
     * @param successor The variable to add.
     */
    inline void add_successor(std::shared_ptr<Variable> successor);

    /**
     * @brief Resets the state of the rule, including the counter.
     */
    void reset();
};


inline void Rule::add_successor(std::shared_ptr<Variable> successor) {
    successors.push_back(successor);
}
    
#endif // CLASSES_H
