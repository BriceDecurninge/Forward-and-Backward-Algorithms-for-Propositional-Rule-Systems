#include <iostream>
#include <vector>
#include <string>
#include "forward.h"


void pre_processing(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules) {
    for (auto& rule : rules) {
        for (auto& antecedent : rule->antecedents) {
            rule->counter += 1;
            
            antecedent->add_rule(rule);
        }
    }
    for (auto& variable : facts_base) {
        variable->assign(VariableState::True);
    }
}

void pre_processing_steps(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules) {
    std::cout << "Starting pre_processing...\n";

    // Link each antecedent to its corresponding rule and initialize counters
    for (auto& rule : rules) {
        std::cout << "Processing rule: " << "\n";
        for (auto& antecedent : rule->antecedents) {
            rule->counter += 1;
            
            std::cout << "Adding rule to antecedent: " << antecedent->to_string() << "\n";
            antecedent->add_rule(rule);
           
        std::cout << "Rule counter set to: " << rule->counter << "\n";
    }

    // Initialize variables in the facts base
    for (auto& variable : facts_base) {
        std::cout << "Initializing variable in facts_base: " << variable->to_string() << "\n";
        variable->assign(VariableState::True);
        std::cout << "Variable state - Name: " << variable->name << ", Used: " << variable->used <<  "\n";
        std::cout << "Variable knows " << variable->rules.size() << " rules.\n";
    }

    std::cout << "Finished pre_processing.\n";
}

}

std::deque<std::shared_ptr<Variable>> forward_pre_processing_queue(std::vector<std::shared_ptr<Variable>>& facts_base, std::vector<std::shared_ptr<Rule>>& rules) {
    for (auto& rule : rules) {
        for (auto& antecedent : rule->antecedents) {
            rule->counter += 1;
            
            antecedent->add_rule(rule);
        }
    }
    for (auto& variable : facts_base) {
        variable->assign(VariableState::True);
    }

    std::deque<std::shared_ptr<Variable>> processing_queue(facts_base.begin(), facts_base.end());

    return processing_queue;
}

bool forward_algorithm_queue(std::deque<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question) {
    
    while (!facts_base.empty()) {
        std::shared_ptr<Variable> variable = facts_base.front();
        facts_base.pop_front();

        if (!variable->is_used()) {
            for (const std::weak_ptr<Rule>& rule_weak : variable->rules) {
                if (std::shared_ptr<Rule> rule = rule_weak.lock()) {
                    --rule->counter;
                    if (rule->counter == 0) {
                        std::shared_ptr<Variable> consequent = rule->consequent;
                        if (consequent->name == question->name) {
                            return true;
                        }
                        facts_base.emplace_back(consequent);
                    }
                }
            }
            variable->used = true;  // Mark variable as used
        }
    }
    return false;  // Default return false if question not found
}


bool forward_algorithm_queue_steps(std::deque<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question) {
    while (!facts_base.empty()) {
        // Get the variable at the front of the queue
        std::shared_ptr<Variable> variable = facts_base.front();
        facts_base.pop_front(); // Remove the variable from the front of the queue

        if (!variable) {
            std::cerr << "Error: Null variable pointer\n";
            return false;
        }

        std::cout << "Processing variable: " << variable->to_string() << "\n";
        std::cout << "Variable state - Name: " << variable->name << ", Used: " << variable->used <<  "\n";

        if (!variable->is_used()) {
            std::cout << "Variable not used yet\n";
            for (const std::weak_ptr<Rule>& rule_weak : variable->rules) {  // Iterate over weak_ptrs to Rule
                if (std::shared_ptr<Rule> rule = rule_weak.lock()) {  // Attempt to lock the weak_ptr
                    std::cout << "Processing rule: " << rule->to_string() << " \n";
                    std::cout << "counter before = " << rule->counter << " \n";
                    rule->counter -= 1;
                    std::cout << "counter after = " << rule->counter << " \n";
                    if (rule->counter == 0) {
                        std::shared_ptr<Variable> consequent = rule->consequent; // Lock the consequent weak_ptr
                        std::cout << "Found consequent: " << consequent->to_string() << "\n";
                        if (consequent->name == question->name) {  // Check name equality
                            std::cout << "Found question: " << consequent->name << "\n";
                            return true;
                        }
                        facts_base.emplace_back(consequent); // Push consequent Variable if needed
                        std::cout << "Added consequent to facts_base: " << consequent->to_string() << "\n";
                    } 
                } else {
                        std::cerr << "Error: Unable to lock consequent weak_ptr\n";
                    }
            }
            std::cout << "Marking variable as used: " << variable->to_string() << "\n";
            if (variable) {  // Ensure variable is still valid
                variable->used = true;  // Mark variable as used
            } else {
                std::cerr << "Error: variable became null unexpectedly\n";
                return false;
            }
        }
    }
    return false;  // Default return false if question not found
}


bool forward_algorithm(std::vector<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question) {
    size_t i = 0;
    while (i < facts_base.size()) {
        
        auto variable = facts_base[i];
        if (!variable) {
            return false;
        }

        if (!variable->is_used()) {
            for (auto& rule_weak : variable->rules) {  // Iterate over weak_ptrs to Rule
                if (auto rule = rule_weak.lock()) {  // Attempt to lock the weak_ptr
                    rule->counter -= 1;
                    if (rule->counter == 0) {
                        auto consequent = rule->consequent; // Lock the consequent weak_ptr
                        std::cout << consequent->to_string(); 
                        if (consequent->name == question->name) {  // Check name equality
                            return true;
                        }
                        facts_base.push_back(consequent); // Push consequent Variable if needed
                        
                    }
                    }
                }
            
            if (variable) {  // Ensure variable is still valid
                variable->used = true;  // Mark variable as used
            } else {
                return false;
            }
        }

        
        i++;  
    }
    return false;  // Default return false if question not found
}


bool forward_algorithm_steps(std::vector<std::shared_ptr<Variable>>& facts_base, std::shared_ptr<Variable>& question) {
    size_t i = 0;
    while (i < facts_base.size()) {
        auto variable = facts_base[i];
        if (!variable) {
            std::cerr << "Error: Null variable pointer at index " << i << "\n";
            return false;
        }

        std::cout << "Processing variable : " << variable->to_string() << "\n";
        std::cout << "Variable state - Name : " << variable->name << ", Used: " << variable->used <<  "\n";

        if (!variable->is_used()) {
            std::cout << "Variable not used yet\n";
            for (auto& rule_weak : variable->rules) {  // Iterate over weak_ptrs to Rule
                if (auto rule = rule_weak.lock()) {  // Attempt to lock the weak_ptr
                    std::cout << "Processing rule :" << rule->to_string() << "counter before = " << rule->counter << " \n";
                    rule->counter -= 1;
                    std::cout << "Processing rule :" << rule->to_string() << "counter after = " << rule->counter << " \n";
                    if (rule->counter == 0) {
                        auto consequent = rule->consequent; // Lock the consequent weak_ptr
                        std::cout << "Found consequent: " << consequent->to_string() << "\n";
                        if (consequent->name == question->name) {  // Check name equality
                            std::cout << "Found question: " << consequent->name << "\n";
                            return true;
                        }
                            facts_base.push_back(consequent); // Push consequent Variable if needed
                            std::cout << "Added consequent to facts_base: " << consequent->to_string() << "\n";
                        } else {
                            std::cerr << "Error: Unable to lock consequent weak_ptr\n";
                        }
                    }
                
            }
            std::cout << "Marking variable as used: " << variable->to_string() << "\n";
            if (variable) {  // Ensure variable is still valid
                variable->used = true;  // Mark variable as used
            } else {
                std::cerr << "Error: variable became null unexpectedly\n";
                return false;
            }
        }
        i++;
    }
    return false;  // Default return false if question not found
}



