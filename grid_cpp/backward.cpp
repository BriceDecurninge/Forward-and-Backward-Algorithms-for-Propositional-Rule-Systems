#include "backward.h"
#include <iostream>
#include <optional>
#include <limits>
#include <variant>


void backward_pre_processing(std::vector<std::shared_ptr<Rule>>& rules, std::vector<std::shared_ptr<Variable>>& facts_base) {
    // Add rules to the consequent's successors
    for (auto& rule : rules) {
        if (rule->consequent) {
            rule->consequent->add_rule(rule);
        } else {
            std::cerr << "Error: Rule has no consequent\n";
        }
    }

    // Assign True to variables in the facts base
    for (auto& variable : facts_base) {
        variable->assign(VariableState::True); 
    }
}



void OR(std::shared_ptr<Variable>& P, ExecutionState& state) {
    P->assign(VariableState::ON);
    bool flag = false;

    P->order = state.counter;
    state.counter++;
   

    for (auto& rule_weak : P->rules) {
        if (auto rule = rule_weak.lock()) {
            auto output = AND(rule, state);

            if (std::holds_alternative<bool>(output) && std::get<bool>(output) == true) {
                P->assign(VariableState::True);
                INVERSE(P, state);
                if (P->order == state.root) {
                    assing_false(state);
                }
                return;
            }

            if (std::holds_alternative<std::vector<std::shared_ptr<Variable>>>(output)) {
                auto& successors = std::get<std::vector<std::shared_ptr<Variable>>>(output);
                for (auto& p : successors) {
                    p->add_successor(rule);
                    if (p->order < state.root) {
                        state.root = p->order.value();
                    }
                }
                flag = true;
                rule->counter = successors.size();
                state.on_list.push_back(P);
            }
        } else {
            std::cerr << "Error: Unable to lock rule weak_ptr\n";
        }
    }

    if (!flag) {
        P->assign(VariableState::False);

        if (P->order == state.root) {
            assing_false(state);
        }
    }
}




std::variant<bool, std::vector<std::shared_ptr<Variable>>> AND(std::shared_ptr<Rule>& R, ExecutionState& state) {
    for (auto& antecedent : R->antecedents) {
        if (antecedent->is_true()) {
            continue;
        }
        if (antecedent->evaluate() == VariableState::None) {
            OR(antecedent, state);
        }
        if (antecedent->evaluate() == VariableState::False) {
            return false;
        }
        if (antecedent->evaluate() == VariableState::ON) {
            R->add_successor(antecedent); 
        }
    }

    if (R->successors.empty()) {
        return true;
    } else {
        return R->successors;
    }
}


void INVERSE(std::shared_ptr<Variable>& P, ExecutionState& state) {
    for (auto& rule_weak : P->successors) {
        if (auto rule = rule_weak.lock()) {
            rule->counter -= 1;
            if (rule->counter == 0) {
                if (rule->consequent) {
                    rule->consequent->assign(VariableState::True);
                    if (!rule->consequent->successors.empty()) {
                        INVERSE(rule->consequent, state);
                    }
                } else {
                    std::cerr << "Error: Rule has no consequent\n";
                }
            }
        } else {
            std::cerr << "Error: Unable to lock rule successor weak_ptr\n";
        }
    }
}



void assing_false(ExecutionState& state) {
    for (auto& p : state.on_list) {
        if (p->value == VariableState::ON) {
            p->assign(VariableState::False);
        }
    }
    state.on_list.clear();
    state.counter = 0;
    state.root = std::numeric_limits<int>::max();
}

bool backward_algorithm(std::shared_ptr<Variable>& Q) {
    ExecutionState state; // Initialize the state here

    if (Q->evaluate() == VariableState::None) {
        OR(Q, state);
    }

    return Q->is_true();
}



void OR_steps(std::shared_ptr<Variable>& P, ExecutionState& state) {
    P->assign(VariableState::ON);
    bool flag = false;

    P->order = state.counter;
    state.counter++;
    std::cout << "OR " << P->to_string() << "\n";

    for (auto& rule_weak : P->rules) {
        if (auto rule = rule_weak.lock()) {
            auto output = AND_steps(rule, state);

            if (std::holds_alternative<bool>(output) && std::get<bool>(output) == true) {
                P->assign(VariableState::True);
                std::cout << P->to_string() << " TRUE " << "\n";
                INVERSE_steps(P, state);
                if (P->order == state.root) {
                    assing_false(state);
                }
                return;
            }

            if (std::holds_alternative<std::vector<std::shared_ptr<Variable>>>(output)) {
                auto& successors = std::get<std::vector<std::shared_ptr<Variable>>>(output);
                for (auto& p : successors) {
                    std::cout << rule->to_string() << " memorizes " << p->to_string() << "\n";
                    p->add_successor(rule);
                    if (p->order < state.root) {
                        state.root = p->order.value();
                    }
                }
                flag = true;
                rule->counter = successors.size();
                state.on_list.push_back(P);
            }
        } else {
            std::cerr << "Error: Unable to lock rule weak_ptr\n";
        }
    }

    if (!flag) {
        P->assign(VariableState::False);
        std::cout << P->to_string() << " FALSE " << "\n";

        if (P->order == state.root) {
            assing_false(state);
        }
    }
}




std::variant<bool, std::vector<std::shared_ptr<Variable>>> AND_steps(std::shared_ptr<Rule>& R, ExecutionState& state) {
    std::cout << "AND " << R->to_string() << "\n";
    for (auto& antecedent : R->antecedents) {
        if (antecedent->is_true()) {
            continue;
        }
        if (antecedent->evaluate() == VariableState::None) {
            OR_steps(antecedent, state);
        }
        if (antecedent->evaluate() == VariableState::False) {
            return false;
        }
        if (antecedent->evaluate() == VariableState::ON) {
            R->add_successor(antecedent); // Successors now use shared_ptr
        }
    }

    if (R->successors.empty()) {
        return true;
    } else {
        return R->successors;
    }
}


void INVERSE_steps(std::shared_ptr<Variable>& P, ExecutionState& state) {
    std::cout << "INVERSING " << P->to_string() << "\n";
    for (auto& rule_weak : P->successors) {
        if (auto rule = rule_weak.lock()) {
            rule->counter -= 1;
            if (rule->counter == 0) {
                if (rule->consequent) {
                    rule->consequent->assign(VariableState::True);
                    if (!rule->consequent->successors.empty()) {
                        INVERSE_steps(rule->consequent, state);
                    }
                } else {
                    std::cerr << "Error: Rule has no consequent\n";
                }
            }
        } else {
            std::cerr << "Error: Unable to lock rule successor weak_ptr\n";
        }
    }
}



void assing_false_steps(ExecutionState& state) {
    for (auto& p : state.on_list) {
        if (p->value == VariableState::ON) {
            p->assign(VariableState::False);
            std::cout << p->to_string() << " FALSE\n";
        }
    }
    state.on_list.clear();
    state.counter = 0;
    state.root = std::numeric_limits<int>::max();
}

bool backward_algorithm_steps(std::shared_ptr<Variable>& Q) {
    ExecutionState state; 

    if (Q->evaluate() == VariableState::None) {
        OR_steps(Q, state);
    }

    return Q->is_true();
}