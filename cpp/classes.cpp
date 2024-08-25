#include "classes.h"

// Global constants
const std::string ou = "∨";
const std::string et = "∧";
const std::string expr = "expression";


// Variable class implementation

//Constructor
Variable::Variable(const std::string& name, VariableState value)
    : name(name),
      value(value),
      used(false) {}

//Destructor
Variable::~Variable(){
    //std::cout<<name <<" variable deleted";
}

void Variable::reset() {
        value = VariableState::None;
        rules.clear();
        used = false;
        successors.clear();
        order = std::nullopt;
    }

bool Variable::operator==(const Variable& other) const {
    return this->name == other.name;
}

// implem of to_string for optional type
std::string Variable::to_string_aux() const {
    std::string description =  "";

    switch (value) {
        case VariableState::None:
            description += "None";
            break;
        case VariableState::True:
            description += "True";
            break;
        case VariableState::False:
            description += "False";
            break;
        case VariableState::ON:
            description += "ON";
            break;
        default:
            description += "Unknown";
            break;
    }

    return description;
}
std::string Variable::to_string() const {
    std::string description = name;
    description += " (" + to_string_aux() + ")";
    return description;
}


Rule::Rule(const std::vector<std::shared_ptr<Variable>>& antecedents, const std::shared_ptr<Variable>& consequent, int counter)
    : antecedents(antecedents), consequent(consequent), counter(counter) {}

//Destructor
Rule::~Rule(){
    //std::cout <<" Rule deleted";
}

void Rule::reset() {
        counter = 0;
        successors.clear();
    }


// Rule to_string implementation
std::string Rule::to_string() const {
    std::string toPrint;
    for (size_t i = 0; i < antecedents.size(); ++i) {
        if (auto antecedent = antecedents[i]) {
            toPrint += antecedent->to_string();
        } else {
            toPrint += "null";
        }
        if (i + 1 < antecedents.size()) {
            toPrint += " ∧ ";
        } else {
            toPrint += " ";
        }
    }
    toPrint += connector + " ";
    if (auto cons = consequent) {
        toPrint += cons->to_string();
    } else {
        toPrint += "null";
    }
    return toPrint;
}







