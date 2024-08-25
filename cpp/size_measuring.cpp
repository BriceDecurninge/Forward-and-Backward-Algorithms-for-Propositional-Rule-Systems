#include "size_measuring.h"
#include <iostream>
#include <numeric>



// Helper function to estimate the memory usage of a vector
template<typename T>
size_t estimate_vector_memory(const std::vector<T>& vec) {
    return sizeof(vec) + (vec.capacity() * sizeof(T));
}

// Helper function to estimate the memory usage of a shared_ptr vector
template<typename T>
size_t estimate_shared_ptr_vector_memory(const std::vector<std::shared_ptr<T>>& vec) {
    return (vec.capacity() * sizeof(std::shared_ptr<T>));
}

// Helper function to estimate the memory usage of a weak_ptr vector
template<typename T>
size_t estimate_weak_ptr_vector_memory(const std::vector<std::weak_ptr<T>>& vec) {
    return (vec.capacity() * sizeof(std::weak_ptr<T>));
}

size_t estimate_variable_memory(const Variable& var) {
    size_t base_size = sizeof(var);

    // Memory details of `std::string name`
    size_t name_size = var.name.capacity(); // Buffer size of the string

    // Memory details of `std::vector<std::weak_ptr<Rule>> rules`
    size_t rules_size = estimate_weak_ptr_vector_memory(var.rules);

    // Total size excluding the vector object itself
    size_t total_size = base_size + name_size + rules_size ;

    std::cout << "Detail memory usage of Variable \"" << var.name << "\":" << std::endl;
    std::cout << "Base size: " << sizeof(var) << " bytes" << std::endl;
    
    std::cout << "Size of std::string: " << sizeof(std::string) << " bytes" << std::endl;
    std::cout << "Size of VariableState: " << sizeof(VariableState) << " bytes" << std::endl;
    std::cout << "Size of std::vector<std::weak_ptr<Rule>>: " << sizeof(std::vector<std::weak_ptr<Rule>>) << " bytes" << std::endl;
    std::cout << "Size of bool: " << sizeof(bool) << " bytes" << std::endl;


    std::cout << "Offset of name: " << offsetof(Variable, name) << " bytes" << std::endl;
    std::cout << "Offset of value: " << offsetof(Variable, value) << " bytes" << std::endl;
    std::cout << "Offset of rules: " << offsetof(Variable, rules) << " bytes" << std::endl;
    std::cout << "Offset of used: " << offsetof(Variable, used) << " bytes" << std::endl;
    std::cout << "Offset of successors: " << offsetof(Variable, successors) << " bytes" << std::endl;
    std::cout << "Offset of order: " << offsetof(Variable, order) << " bytes" << std::endl;
    
    std::cout << "Total size of Variable: " << sizeof(Variable) << " bytes" << std::endl;

    std::cout << "Size of name: " << name_size << " bytes" << std::endl;
    std::cout << "Size of rules vector: " << rules_size << " bytes" << std::endl;
   
    std::cout << "Total size: " << total_size << " bytes" << std::endl;
    
    return total_size;
}

size_t estimate_rule_memory(const Rule& rule) {
    size_t base_size = sizeof(rule);

    // Memory details of `std::vector<std::shared_ptr<Variable>> antecedents`
    size_t antecedents_size = estimate_shared_ptr_vector_memory(rule.antecedents);

    // Memory details of `std::string connector`
    size_t connector_size = rule.connector.capacity();

    // Memory details of `std::vector<std::shared_ptr<Variable>> successors`
    size_t successors_size = estimate_shared_ptr_vector_memory(rule.successors);

    // Memory details of `int counter`
    size_t counter_size = sizeof(rule.counter);

    // Total size excluding the vector objects themselves
    size_t total_size = base_size + antecedents_size + connector_size + successors_size + counter_size ;

    std::cout << "Detail memory usage of Rule \"" << rule.connector << "\":" << std::endl;
    std::cout << "Base size: " << sizeof(rule) << " bytes" << std::endl;
    std::cout << "Size of antecedents vector: " << antecedents_size << " bytes" << std::endl;
    std::cout << "Size of connector: " << connector_size << " bytes" << std::endl;
    std::cout << "Size of successors vector: " << successors_size << " bytes" << std::endl;
    std::cout << "Size of counter: " << counter_size << " bytes" << std::endl;
    std::cout << "Total size: " << total_size << " bytes" << std::endl;

    std::cout << "Offset of antecedents: " << offsetof(Rule, antecedents) << " bytes" << std::endl;
    std::cout << "Offset of connector: " << offsetof(Rule, connector) << " bytes" << std::endl;
    std::cout << "Offset of consequent: " << offsetof(Rule, consequent) << " bytes" << std::endl;
    std::cout << "Offset of counter: " << offsetof(Rule, counter) << " bytes" << std::endl;
    std::cout << "Offset of successors: " << offsetof(Rule, successors) << " bytes" << std::endl;
    
    std::cout << "Total size of Rule: " << sizeof(Rule) << " bytes" << std::endl;

    return total_size;
}

int main() {
    // Create Variables
    std::shared_ptr<Variable> P1 = std::make_shared<Variable>("P1");
    std::shared_ptr<Variable> P2 = std::make_shared<Variable>("P2");
    std::shared_ptr<Variable> P3 = std::make_shared<Variable>("P3");
    std::shared_ptr<Variable> P4 = std::make_shared<Variable>("P4");

    // Create Rules
    auto Rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{P1, P2}, P3,0);
    auto Rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{P1}, P4,0);
    auto Rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{P2}, P4,0);
    

    std::vector<std::shared_ptr<Rule>> rules = {Rule1,Rule2,Rule3};

    for (auto& rule : rules) {
        for (auto& antecedent : rule->antecedents) {
            rule->counter += 1;
            
            antecedent->add_rule(rule);
        }
    }



    

    // Measure sizes using sizeof
    std::cout << "Base size of Variable: " << sizeof(Variable) << " bytes" << std::endl;
    std::cout << "Base size of Rule: " << sizeof(Rule) << " bytes" << std::endl;
    std::cout << "Base size of s_p(Variable): " << sizeof(std::shared_ptr<Variable>) << " bytes" << std::endl;
    std::cout << "Base size of w_p(Rule): " << sizeof(std::weak_ptr<Rule>) << " bytes" << std::endl;
    
    
    // Estimate total memory usage
    std::cout << "Total memory usage of P1: " << estimate_variable_memory(*P1) << " bytes" << std::endl;
    std::cout << "Total memory usage of P2: " << estimate_variable_memory(*P2) << " bytes" << std::endl;
    std::cout << "Total memory usage of P3: " << estimate_variable_memory(*P3) << " bytes" << std::endl;
    std::cout << "Total memory usage of P4: " << estimate_variable_memory(*P4) << " bytes" << std::endl;

    std::cout << "Total memory usage of Rule1: " << estimate_rule_memory(*Rule1) << " bytes" << std::endl;
    std::cout << "Total memory usage of Rule2: " << estimate_rule_memory(*Rule2) << " bytes" << std::endl;
    std::cout << "Total memory usage of Rule3: " << estimate_rule_memory(*Rule3) << " bytes" << std::endl;

    return 0;
}