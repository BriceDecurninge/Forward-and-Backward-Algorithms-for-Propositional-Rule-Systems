#include "benchmark_generator.h"
#include <cmath>
#include <random>
#include <chrono>

std::vector<std::vector<std::string>> generate_rules_benchmark1(int k, int n, std::vector<std::string>& variables_base) {
    std::vector<std::vector<std::string>> rules;
    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < n; ++j) {
            std::string antecedent = "P" + std::to_string(j) + "." + std::to_string(i);
            std::string consequent = "P" + std::to_string(j + 1) + "." + std::to_string(i);
            rules.push_back({antecedent, consequent});
            variables_base.push_back(antecedent);
            variables_base.push_back(consequent);
        }
    }
    return rules;
}

std::vector<std::vector<std::string>> generate_rules_benchmark2(int k, int n) {
    std::vector<std::vector<std::string>> rules;

    for (int j = 0; j < n; ++j) {

        for (int i = 0; i < k; ++i) {
            std::string antecedent;
            std::string consequent;
            
            if (j%2 == 0) {
                antecedent = "P" + std::to_string(j/2);
                consequent = "P" + std::to_string(j/2) + "." + std::to_string(i);
            }

            else {
                consequent = "P" + std::to_string((j+1)/2);
                antecedent = "P" + std::to_string((j-1)/2) + "." + std::to_string(i);
            }

            rules.push_back({antecedent, consequent});
            
            
            
        }
        
    }
        

    return rules;
}


std::vector<std::vector<std::string>> generate_rules_benchmark3(int k, bool oriented) {
    std::vector<std::vector<std::string>> rules;

    for (int i = 0; i < k; ++i) {
        std::string antecedent = "P" + std::to_string(i);
        if (oriented) {
            for (int j = i + 1; j < k; ++j) {
                std::string consequent = "P" + std::to_string(j);
                rules.push_back({antecedent, consequent});
            }
        } else {
            for (int j = 0; j < k+1; ++j) {
                if (i != j) {
                    std::string consequent = "P" + std::to_string(j);
                    rules.push_back({antecedent, consequent});
                }
            }
        }
    }

    // Utilisez std::shuffle pour mélanger les rules
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::shuffle(rules.begin(), rules.end(), std::default_random_engine(seed));


    return rules;
}

std::vector<std::vector<std::string>> generate_rules_benchmark3_worst(int k) {
    std::vector<std::vector<std::string>> rules;

    for (int i = k; i > -1; --i) {
        std::string antecedent = "P" + std::to_string(i);
        
       
        for (int j = 0; j < k+1; ++j) {
            if (i != j) {
                std::string consequent = "P" + std::to_string(j);
                rules.push_back({antecedent, consequent});
            }
        }
    
    }

    return rules;
}

std::vector<std::vector<std::string>> generate_rules_benchmark4(int k) {
    std::vector<std::vector<std::string>> rules;

    for (int i = 1; i < k; ++i) {
        std::string antecedents;
        for (int j = i + 1; j <= k; ++j) {
            std::string antecedent = "P" + std::to_string(j);
            antecedents += antecedent;
            if (j < k) {
                antecedents += "∧";
            }
            
        }
        std::string consequent = "P" + std::to_string(i);
        rules.push_back({antecedents, consequent});
    }

    return rules;
}


std::vector<std::vector<std::string>> generate_rules_benchmark5(int k, int n) {
    std::vector<std::vector<std::string>> rules;

    for (int i = 1; i <= n; ++i) {
        int index = 0;
        for (int j = 0; j < std::pow(k, i); j += k) {
            std::string antecedent = "P" + std::to_string(i) + "." + std::to_string(index);
            for (int l = 0; l < k; ++l) {
                std::string consequent = "P" + std::to_string(i + 1) + "." + std::to_string(j + l);
                rules.push_back({antecedent, consequent});
            }
            ++index;
        }
    }
    return rules;
}

std::vector<std::vector<std::string>> generate_rules_benchmark(int num_bench, int k, int n, std::vector<std::string>& variable_base) {
    switch(num_bench){
        case 1:
            return generate_rules_benchmark1(k,n,variable_base);
        case 2:
            return generate_rules_benchmark2(k,n);
        case 3:
            return generate_rules_benchmark3(k,false);
        case 4:
            return generate_rules_benchmark4(k);
        case 5:
            return generate_rules_benchmark5(k,n);
        default:
            return {};
    }
}

std::vector<std::vector<std::string>> generate_rules_benchmark_worst(int num_bench, int k, int n) {
    switch(num_bench){
        case 3:
            return generate_rules_benchmark3_worst(k);
        default:
            return {};
    }
}





std::vector<std::string> generate_fb_benchmark(int num_bench, const std::vector< std::vector<std::string>>& rules, int n) {
    std::vector<std::string> FactsBase;
    if (num_bench == 1) {
        for (size_t rule = 0; rule < rules.size(); rule += n) {
            FactsBase.push_back(rules[rule][0]);
        }
    } else if (num_bench == 2 || num_bench == 3) {
        if (!rules.empty()) {
            //FactsBase.push_back(rules[0][0]);
            FactsBase.push_back("P0");

        }
    } else if (num_bench == 4) {
        size_t length = rules.size();
        if (!rules.empty()) {
            FactsBase.push_back(rules[length - 1][0]);
        }
    } else if (num_bench == 5) {
        if (!rules.empty()) {
            FactsBase.push_back(rules[0][0]);
        }
    }
    return FactsBase;
}
//Not well done at all. Should remove variable_base
std::string generate_question(const std::vector<std::string>& listOfQuestions, bool cheat) {
    if (listOfQuestions.empty()) {
        return "";
    }
    std::string question = listOfQuestions[std::rand() % listOfQuestions.size()];
    if (cheat) {
        question = listOfQuestions.back();
    }
    return question;
}

std::string generate_question1(int num_bench, int k, int n) {
    
    std::string question = "";
    
    if (num_bench == 1){
        question = "P" + std::to_string(n) + "." + std::to_string(k-1);
    }

    if (num_bench == 2){
        if (n%2 == 0){
            question = "P" + std::to_string(n/2); 
        }
        else{
            question = "P" + std::to_string((n-1)/2) + "." + std::to_string(k-1);
        }
        
    }

    if (num_bench == 3){
        question = "P" + std::to_string(k);
    }

    if (num_bench == 4){
        question = "P1";
    }

    if (num_bench == 5){
        question = "P" + std::to_string(n+1) + "." + std::to_string(int(pow(k,n)) - 1);
    }

    return question;

}

/*
std::unordered_map<std::string, std::any> generate_benchmark2(int num_bench, int k, int n, bool oriented) {

    std::vector<std::string> variables_base = {};
    std::unordered_map<std::string, std::any> data;

    data["rules"] = generate_rules_benchmark(num_bench, k, n, variables_base);

    
    auto rulesIt = data.find("rules");
    
    if (rulesIt != data.end()) {

        const std::vector<std::vector<std::string>>& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(rulesIt->second);
        data["facts base"] = generate_fb_benchmark(num_bench, rules, n );
    
    } else {
        std::cerr << "Error: Unable to find element with key rules\n";
    }

    
    //data["question"] = generate_question(variables_base);
    data["question"] = generate_question1(num_bench,k,n);

    return data;
}
*/



std::unordered_map<std::string, std::shared_ptr<std::any>> generate_benchmark(int num_bench, int k, int n) {
    
    std::vector<std::string> variables_base;
    std::unordered_map<std::string, std::shared_ptr<std::any>> data;

    data["rules"] = std::make_shared<std::any>(generate_rules_benchmark(num_bench, k, n, variables_base));

    auto rulesIt = data.find("rules");

    if (rulesIt != data.end()) {
        const std::vector<std::vector<std::string>>& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(*rulesIt->second);
        data["facts base"] = std::make_shared<std::any>(generate_fb_benchmark(num_bench, rules, n));
    } else {
        std::cerr << "Error: Unable to find element with key rules\n";
    }

    data["question"] = std::make_shared<std::any>(generate_question1(num_bench, k, n));

    return data;
}

std::unordered_map<std::string, std::shared_ptr<std::any>> generate_benchmark_worst(int num_bench, int k, int n) {
    
    std::vector<std::string> variables_base;
    std::unordered_map<std::string, std::shared_ptr<std::any>> data;

    data["rules"] = std::make_shared<std::any>(generate_rules_benchmark_worst(num_bench, k, n));

    auto rulesIt = data.find("rules");

    if (rulesIt != data.end()) {
        const std::vector<std::vector<std::string>>& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(*rulesIt->second);
        data["facts base"] = std::make_shared<std::any>(generate_fb_benchmark(num_bench, rules, n));
    } else {
        std::cerr << "Error: Unable to find element with key rules\n";
    }

    data["question"] = std::make_shared<std::any>(generate_question1(num_bench, k, n));

    return data;
}



