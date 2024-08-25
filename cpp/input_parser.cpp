#include "input_parser.h"



// Updated create_set function
std::unordered_map<std::string, std::shared_ptr<std::any>> create_set(const std::unordered_map<std::string, std::shared_ptr<std::any>>& data) {
    std::unordered_map<std::string, std::shared_ptr<Variable>> variables;

    if (data.empty()) {
        throw std::invalid_argument("Input data is empty");
    }

    auto rulesIt = data.find("rules");
    auto fbIt = data.find("facts base");
    auto questionIt = data.find("question");

    if (rulesIt == data.end() || fbIt == data.end() || questionIt == data.end()) {
        throw std::invalid_argument("Bench is missing required keys");
    }

    const auto& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(*rulesIt->second);
    const auto& fb = std::any_cast<const std::vector<std::string>&>(*fbIt->second);
    const auto& question = std::any_cast<const std::string&>(*questionIt->second);

    // Parsing rules
    std::vector<std::shared_ptr<Rule>> rules_parsed;
    for (const auto& rule : rules) {
        rules_parsed.push_back(vector_to_rule(rule, variables));
    }

    // Create the result map
    std::unordered_map<std::string, std::shared_ptr<std::any>> result;
    result["rules"] = std::make_shared<std::any>(rules_parsed);
    result["facts base"] = std::make_shared<std::any>(create_fb(fb, variables));
    result["question"] = std::make_shared<std::any>(create_question(question, variables)); 

    return result;
}

// shared_ptr <Rule>
std::shared_ptr<Rule> vector_to_rule(const std::vector<std::string>& listRule, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables) {
    
    //Need to add parse_rule

    std::unordered_map<std::string,std::any> parsed_rule = parse_rule(listRule);

   
    // Parsing antecedents and consequent
    auto antIt = parsed_rule.find("antecedents");
    auto consIt = parsed_rule.find("consequent");

    if (antIt == parsed_rule.end() || consIt == parsed_rule.end()) {
        throw std::invalid_argument("parsed_rule is missing required keys");
    }

    const std::vector<std::string>& ant_str = std::any_cast<const std::vector<std::string>&>(antIt->second);
    const std::string& csq_str = std::any_cast<const std::string&>(consIt->second);
    


    //Simple version where there is only one antecedent
    //std::vector<std::string > ant_str =  {listRule[0]};
    //std::string csq_str = listRule[1];
    //std::vector<std::weak_ptr<Variable>> ants = create_ant(ant_str, variables);
    //std::weak_ptr<Variable> csq = createCsqObj(csq_str, variables);

    std::vector<std::shared_ptr<Variable>> ants = create_ant(ant_str, variables);
    std::shared_ptr<Variable> csq = create_csq(csq_str, variables);
    return std::make_shared<Rule>(ants, csq, 0);
    
}





std::vector<std::shared_ptr<Variable>> create_ant(const std::vector<std::string>& list, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables) {
    std::vector<std::shared_ptr<Variable>> antList;
    std::shared_ptr<Variable> ant;
    for (const auto& antStr : list) {
        if (variables.find(antStr) == variables.end()) {
            // Create a new Variable and store it in the map as a shared_ptr
            std::shared_ptr<Variable> ant = std::make_shared<Variable>(antStr);
            variables[antStr] = ant;
        }
        // Add the shared_ptr to the antList

        antList.push_back(variables[antStr]);
    }

    return antList;
}

std::shared_ptr<Variable> create_csq(const std::string& var, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables) {
    if (variables.find(var) == variables.end()) {
        // Create a new Variable and store it in the map as a shared_ptr
        std::shared_ptr<Variable> csq = std::make_shared<Variable>(var);
        variables[var] = csq;
    
    } 
    return variables[var];
    
}

std::shared_ptr<Variable> create_question(const std::string& question, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables) {
     if (variables.find(question) == variables.end()) {
        // Create a new Variable and store it in the map as a shared_ptr
        std::shared_ptr<Variable> csq = std::make_shared<Variable>(question);
        variables[question] = csq;
        return csq;
    
    } 
    std::shared_ptr<Variable> csq = variables[question];
    return csq;
    

}
std::vector<std::shared_ptr<Variable>> create_fb(const std::vector<std::string>& list, std::unordered_map<std::string, std::shared_ptr<Variable>>& variables) {
    std::vector<std::shared_ptr<Variable>> fbList;
    for (const auto& varStr : list) {
        if (variables.find(varStr) == variables.end()) {
            // Create a new Variable and store it in the map as a shared_ptr
            std::shared_ptr<Variable> var = std::make_shared<Variable>(varStr);
            variables[varStr] = var;
        }
        // Add the shared_ptr to the fbList
        fbList.push_back(variables[varStr]);
    }
    return fbList;
}


std::vector<std::string> parse_connector(std::string string, std::string connector) {
    std::vector<std::string> result;
    std::string delimiter = connector;
    size_t pos = 0;
    std::string token;
    while ((pos = string.find(delimiter)) != std::string::npos) {
        token = string.substr(0, pos);
        result.push_back(token);
        string.erase(0, pos + delimiter.length());
    }
    result.push_back(string);
    return result;
}


std::unordered_map<std::string, std::any> parse_rule(std::vector<std::string> rule) {
    std::unordered_map<std::string, std::any> result;
    std::string antecedentsString = rule[0];
    std::string consequent = rule[1];

    std::vector<std::string> antecedents = parse_connector(antecedentsString,"∧");
    result["antecedents"] = antecedents;
    result["consequent"] = consequent;

    return result;
}
