#include "tests.h"
#include "forward.h"
#include "backward.h"

#include "benchmark_generator.h"
#include "input_parser.h"

#include "json_parser.h"

#define PRINT_TEST_NAME() std::cout << "\n\nRunning Test: " << __FUNCTION__ << "\n\n" << std::endl;




void reset_state(const std::vector<std::shared_ptr<Rule>>& rules, const std::vector<std::shared_ptr<Variable>>& facts_base,const std::shared_ptr<Variable>& question) {
    for (auto& rule : rules) {
        rule->reset();
        
        for (auto& antecedent : rule->antecedents) {
            antecedent->reset();
        }
        
        if (rule->consequent) {
            rule->consequent->reset();
        }
    }
    
    for (auto& variable : facts_base) {
        variable->reset(); 
    }

    question -> reset();
}

void run_test(const std::string& algorithm, std::vector<std::shared_ptr<Variable>> facts_base, std::vector<std::shared_ptr<Rule>> rules, std::shared_ptr<Variable> question) {
    
    
    if (algorithm == "forward" || algorithm == "both") {
        std::cout << "\nTesting Forward Algorithm:" << std::endl;
        std::deque fb_q = forward_pre_processing_queue(facts_base,rules);
        bool forward_result = forward_algorithm_queue_steps(fb_q,question);
        std::cout << "Forward Result: " << forward_result << "\n" << std::endl;
    }

    reset_state(rules,facts_base,question);

    if (algorithm == "backward" || algorithm == "both") {
        std::cout << "Testing Backward Algorithm:" << std::endl;
        backward_pre_processing(rules, facts_base);
        bool backward_result = backward_algorithm_steps(question);
        std::cout << "Backward Result: " << backward_result << "\n" << std::endl;
    }
}

void test_simple_deduction1(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A");
    auto varB = std::make_shared<Variable>("B");
    auto varQ = std::make_shared<Variable>("Q");

    auto rule = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varQ);

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB};
    std::vector<std::shared_ptr<Rule>> rules{rule};

    run_test(algorithm,facts_base,rules,varQ);

}



void test_simple_deduction2(const std::string& algorithm) {
    PRINT_TEST_NAME()

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);


    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA,varB}, varD, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC}, varD, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA,varB};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2};

    run_test(algorithm,facts_base,rules,varD);


}


void test_simple_deduction3(const std::string& algorithm) {
    PRINT_TEST_NAME()

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);


    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA,varB}, varQ, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC}, varQ, 0);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varD}, varB, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA,varD};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3};

    run_test(algorithm,facts_base,rules,varQ);
    
}

void test_simple_deduction4(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varC, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC, varD}, varQ, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB, varD};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2};

    run_test(algorithm,facts_base,rules,varQ);
}




void test_simple_deduction5(const std::string& algorithm) {
    PRINT_TEST_NAME()

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);


    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA,varB,varC}, varQ, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA,varB}, varC, 0);
    

    std::vector<std::shared_ptr<Variable>> facts_base{varA,varB};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2};

    run_test(algorithm,facts_base,rules,varQ);

}


void test_simple_deduction6(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A");
    auto varB = std::make_shared<Variable>("B");
    auto varC = std::make_shared<Variable>("C");
    auto varD = std::make_shared<Variable>("D");
    auto varQ = std::make_shared<Variable>("Q");

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA}, varQ);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varB, varC}, varQ);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varD}, varQ);

    std::vector<std::shared_ptr<Variable>> facts_base{varB, varC};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3};

    run_test(algorithm,facts_base,rules,varQ);
}


void test_deduction_with_cycle1(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A");
    auto varB = std::make_shared<Variable>("B");
    auto varC = std::make_shared<Variable>("C");
    auto varQ = std::make_shared<Variable>("Q");

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA}, varB);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varB}, varC);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC}, varA);  // Cycle
    auto rule4 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC}, varQ);

    std::vector<std::shared_ptr<Variable>> facts_base{varA};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3, rule4};

    run_test(algorithm,facts_base,rules,varQ);
}


void test_deduction_with_cycle2(const std::string& algorithm) {
    PRINT_TEST_NAME();
    
    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varE = std::make_shared<Variable>("E", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varC, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varB, varC}, varA, 0); 
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varE}, varQ, 0);
    auto rule4 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC, varD}, varE, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB, varD};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3, rule4};

    run_test(algorithm,facts_base,rules,varQ);
}


void test_deduction_with_multiple_cycles(const std::string& algorithm) {
    PRINT_TEST_NAME();
    
    auto varA1 = std::make_shared<Variable>("A1", VariableState::None);
    auto varA2 = std::make_shared<Variable>("A2", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varE = std::make_shared<Variable>("E", VariableState::None);
    auto varF = std::make_shared<Variable>("F", VariableState::None);
    auto varG = std::make_shared<Variable>("G", VariableState::None);
    auto varH = std::make_shared<Variable>("H", VariableState::None);
    auto varI = std::make_shared<Variable>("I", VariableState::None);
    auto varJ = std::make_shared<Variable>("J", VariableState::None);
    auto varK = std::make_shared<Variable>("K", VariableState::None);
    auto varL = std::make_shared<Variable>("L", VariableState::None);
    auto varM = std::make_shared<Variable>("M", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);

    
    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA1, varB}, varC, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC, varD}, varE, 0);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varE, varF}, varG, 0);
    auto rule4 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varG}, varA1, 0); // First Cycle
    auto rule5 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varG, varH}, varI, 0);
    auto rule6 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varI}, varQ, 0); 
    auto rule7 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varJ, varK}, varB, 0);
    auto rule8 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varB}, varJ, 0); // Second Cycle
    auto rule9 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varK, varL}, varM, 0);
    auto rule10 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varM, varQ}, varK, 0); // Third Cycle
    auto rule11 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA2}, varL, 0);
    auto rule12 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varL, varI}, varD, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA2, varE, varF, varH};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12};

    run_test(algorithm,facts_base,rules,varQ);
}



void test_non_deducible1(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A");
    auto varB = std::make_shared<Variable>("B");
    auto varC = std::make_shared<Variable>("C");
    auto varQ = std::make_shared<Variable>("Q");

    auto rule = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varC);

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB};
    std::vector<std::shared_ptr<Rule>> rules{rule};

    run_test(algorithm,facts_base,rules,varQ);  // Q should not be deducible
}


void test_non_deducible2(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varE = std::make_shared<Variable>("E", VariableState::None);
    auto varF = std::make_shared<Variable>("F", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varC, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC, varD}, varE, 0);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varE, varF}, varQ, 0);

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB, varD};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3};

   
    run_test(algorithm,facts_base,rules,varQ);    
}

void test_non_deducible_with_cycle(const std::string& algorithm) {
    PRINT_TEST_NAME();

    auto varA = std::make_shared<Variable>("A", VariableState::None);
    auto varB = std::make_shared<Variable>("B", VariableState::None);
    auto varC = std::make_shared<Variable>("C", VariableState::None);
    auto varD = std::make_shared<Variable>("D", VariableState::None);
    auto varE = std::make_shared<Variable>("E", VariableState::None);
    auto varF = std::make_shared<Variable>("F", VariableState::None);
    auto varQ = std::make_shared<Variable>("Q", VariableState::None);

    auto rule1 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varA, varB}, varC, 0);
    auto rule2 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varC, varD}, varE, 0);
    auto rule3 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varE, varF}, varQ, 0);
    auto rule4 = std::make_shared<Rule>(std::vector<std::shared_ptr<Variable>>{varB}, varA, 0); // Cycle

    std::vector<std::shared_ptr<Variable>> facts_base{varA, varB, varD};
    std::vector<std::shared_ptr<Rule>> rules{rule1, rule2, rule3, rule4};

    run_test(algorithm,facts_base,rules,varQ);
}




//// TESTS FOR BENCHMARKS ////

void test_generate_benchmark(int num_bench, int k, int n) {
    PRINT_TEST_NAME()
    
    std::unordered_map<std::string, std::shared_ptr<std::any>> data = generate_benchmark(num_bench, k, n);

    // Retrieve and print "rules"
    auto rulesIt = data.find("rules");
    if (rulesIt != data.end()) {
        const std::vector<std::vector<std::string>>& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(*rulesIt->second);
        std::cout << "Rules:" << std::endl;
        for (const auto& ruleSet : rules) {
            for (const auto& rule : ruleSet) {
                std::cout << rule << " ";
            }
            std::cout << std::endl;
        }
    } else {
        std::cerr << "Error: Unable to find element with key rules\n";
    }

    // Retrieve and print "facts base"
    auto fbIt = data.find("facts base");
    if (fbIt != data.end()) {
        const std::vector<std::string>& factsBase = std::any_cast<const std::vector<std::string>&>(*fbIt->second);
        std::cout << "Facts Base:" << std::endl;
        for (const auto& fact : factsBase) {
            std::cout << fact << " ";
        }
        std::cout << std::endl;
    } else {
        std::cerr << "Error: Unable to find element with key facts base\n";
    }

    // Retrieve and print "question"
    auto questionIt = data.find("question");
    if (questionIt != data.end()) {
        const std::string& question = std::any_cast<const std::string&>(*questionIt->second);
        std::cout << "Question: " << question << std::endl;
    } else {
        std::cerr << "Error: Unable to find element with key question\n";
    }
}


void test_generate_and_process_benchmark(const std::string& algorithm,int num_bench, int k, int n) {
    PRINT_TEST_NAME();

    
    auto data = generate_benchmark(num_bench,k,n);

    // Step 2: Process the data using create_set
    auto processed_data = create_set(data);

    // Retrieve the processed data
    auto rulesIt = processed_data.find("rules");
    auto fbIt = processed_data.find("facts base");
    auto questionIt = processed_data.find("question");

    if (rulesIt == processed_data.end() || fbIt == processed_data.end() || questionIt == processed_data.end()) {
        throw std::runtime_error("Processed data is missing required keys");
    }

    // Step 3: Extract the data for pre-processing and the main algorithm
    auto rules = std::any_cast<std::vector<std::shared_ptr<Rule>>>(*rulesIt->second);
    auto facts_base = std::any_cast<std::vector<std::shared_ptr<Variable>>>(*fbIt->second);
    auto question = std::any_cast<std::shared_ptr<Variable>>(*questionIt->second);

    
    run_test(algorithm,facts_base,rules,question);
   

}


/// TESTS JSON

void test_print_json(const std::string& filename) {
    PRINT_TEST_NAME();

    std::unordered_map<std::string, std::shared_ptr<std::any>> data = parse_json(filename);

    // Retrieve and print "rules"
    auto rulesIt = data.find("rules");
    if (rulesIt != data.end()) {
        const std::vector<std::vector<std::string>>& rules = std::any_cast<const std::vector<std::vector<std::string>>&>(*rulesIt->second);
        std::cout << "Rules:" << std::endl;
        for (const auto& ruleSet : rules) {
            for (const auto& rule : ruleSet) {
                std::cout << rule << " ";
            }
            std::cout << std::endl;
        }
    } else {
        std::cerr << "Error: Unable to find element with key rules\n";
    }

    // Retrieve and print "facts base"
    auto fbIt = data.find("facts base");
    if (fbIt != data.end()) {
        const std::vector<std::string>& factsBase = std::any_cast<const std::vector<std::string>&>(*fbIt->second);
        std::cout << "Facts Base:" << std::endl;
        for (const auto& fact : factsBase) {
            std::cout << fact << " ";
        }
        std::cout << std::endl;
    } else {
        std::cerr << "Error: Unable to find element with key facts base\n";
    }

    // Retrieve and print "question"
    auto questionIt = data.find("question");
    if (questionIt != data.end()) {
        const std::string& question = std::any_cast<const std::string&>(*questionIt->second);
        std::cout << "Question: " << question  << std::endl;
    } else {
        std::cerr << "Error: Unable to find element with key question\n";
    }
}

void test_json (const std::string& algorithm, const std::string& filename) {
    PRINT_TEST_NAME();

    std::cout << filename << "\n\n" ;

    auto data = parse_json(filename);
    auto processed_data = create_set(data);

     // Retrieve the processed data
    auto rulesIt = processed_data.find("rules");
    auto fbIt = processed_data.find("facts base");
    auto questionIt = processed_data.find("question");

    if (rulesIt == processed_data.end() || fbIt == processed_data.end() || questionIt == processed_data.end()) {
        throw std::runtime_error("Processed data is missing required keys");
    }

    // Step 3: Extract the data for pre-processing and the main algorithm
    auto rules = std::any_cast<std::vector<std::shared_ptr<Rule>>>(*rulesIt->second);
    auto facts_base = std::any_cast<std::vector<std::shared_ptr<Variable>>>(*fbIt->second);
    auto question = std::any_cast<std::shared_ptr<Variable>>(*questionIt->second);


    std::cout << "Rules:" << std::endl;
    for (const auto& rule : rules) {
        std::cout << rule->to_string() << " \n";
    }

    // Print the facts base
    std::cout << "\nFacts Base:" << std::endl;
    for (const auto& fact : facts_base) {
        std::cout << fact->to_string();
    }
    std::cout << "\n";

    run_test(algorithm,facts_base,rules,question);


}



std::vector<int> generate_sizes(int start, int end, int step) {
    std::vector<int> sizes;
    for (int i = start; i <= end; i += step) {
        sizes.push_back(i);
    }
    return sizes;
}


int main() {
    
    //test_simple_deduction("both");
    //test_deduction_with_cycle("both");
   //test_print_json("test1.json");
   test_json("both","test1.json");
   test_json("both","test2.json");
   test_json("both","test3.json");
   test_json("both","test4.json");
   test_json("both","test5.json");

    
    

    return 0;
}