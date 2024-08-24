#include "time_measuring.h"
#include "benchmark_generator.h"
#include "input_parser.h"
#include "forward.h"
#include "backward.h"

#include <fstream>
#include <iostream>
#include <chrono>
#include <any>
#include <map>
#include <string>
#include <numeric>
#include <stdexcept>




void reset_state(const std::vector<std::shared_ptr<Rule>>& rules, const std::vector<std::shared_ptr<Variable>>& facts_base,const std::shared_ptr<Variable>& question) {
    for (auto& rule : rules) {
        rule->reset();
        
        for (auto& antecedent : rule->antecedents) {
            antecedent->reset();
        }
        // Reset the consequent of the rule
        if (rule->consequent) {
            rule->consequent->reset();
        }
    }
    
    for (auto& variable : facts_base) {
        variable->reset(); 
    }

    question -> reset();
}


std::vector<std::pair<int, double>> measure_execution_time(std::string alg, int num_bench, int k, const std::vector<int>& sizes, int repeat) {
    std::vector<std::pair<int, double>> execution_times;

    for (int n : sizes) {

        std::cout << "Processing size : " << n << "\n";
        
        auto data = generate_benchmark(num_bench,k,n);
        auto processed_data = create_set(data);

        // Retrieve the processed data
        auto rulesIt = processed_data.find("rules");
        auto fbIt = processed_data.find("facts base");
        auto questionIt = processed_data.find("question");

        if (rulesIt == processed_data.end() || fbIt == processed_data.end() || questionIt == processed_data.end()) {
            throw std::runtime_error("Processed data is missing required keys");
        }

        auto original_rules = std::any_cast<std::vector<std::shared_ptr<Rule>>>(*rulesIt->second);
        auto original_facts_base = std::any_cast<std::vector<std::shared_ptr<Variable>>>(*fbIt->second);
        auto original_question = std::any_cast<std::shared_ptr<Variable>>(*questionIt->second);

        std::vector<double> times;


        std::vector<std::shared_ptr<Rule>> rules = original_rules;
        std::vector<std::shared_ptr<Variable>> facts_base = original_facts_base;
        std::shared_ptr<Variable> question = original_question;


        for (int i = 0; i < repeat; ++i) {
            
            // Reset the state before each run
            reset_state(rules, facts_base,question);

            if (alg == "forward"){
                std::deque fb_q = forward_pre_processing_queue(facts_base,rules);
                
                auto start = std::chrono::high_resolution_clock::now();
                forward_algorithm_queue(fb_q,question);
                auto end = std::chrono::high_resolution_clock::now();
                
                std::chrono::duration<double> duration = end - start;
                times.push_back(duration.count());

            }

            else if(alg == "backward"){
                backward_pre_processing(rules, facts_base);
                
                auto start = std::chrono::high_resolution_clock::now();
                backward_algorithm(question); // change the name
                auto end = std::chrono::high_resolution_clock::now();
                
                std::chrono::duration<double> duration = end - start;
                times.push_back(duration.count());
            }

            else {
                throw std::invalid_argument("Algorithm can be either forward or backward");
            }
            
            
                 
        }

        double average_time = std::accumulate(times.begin(), times.end(), 0.0) / times.size();
        execution_times.push_back({n, average_time});
    }

    return execution_times;
}


std::pair< std::vector<std::pair<int, double>>,std::vector<std::pair<int, double>> > measure_both_execution_time(int num_bench, int k, const std::vector<int>& sizes, int repeat) {
    
    std::vector<std::pair<int, double>> forward_execution_times;
    std::vector<std::pair<int, double>> backward_execution_times;

    for (int n : sizes) {

        std::cout << "Processing size : " << n << "\n";
        
        // Generate the data using generate_benchmark once for each size
        
        std::unordered_map<std::string, std::shared_ptr<std::any>> data;
        switch (num_bench){
            case 3:
                //data = generate_benchmark_worst(num_bench,n,0);
                data = generate_benchmark(num_bench,n,0);
                break;
            case 4:
                data = generate_benchmark(num_bench,n,0);
                break;
            default:
                data = generate_benchmark(num_bench,k,n);


        }
        

        auto processed_data = create_set(data);

        // Retrieve the processed data
        auto rulesIt = processed_data.find("rules");
        auto fbIt = processed_data.find("facts base");
        auto questionIt = processed_data.find("question");

        if (rulesIt == processed_data.end() || fbIt == processed_data.end() || questionIt == processed_data.end()) {
            throw std::runtime_error("Processed data is missing required keys");
        }

        auto original_rules = std::any_cast<std::vector<std::shared_ptr<Rule>>>(*rulesIt->second);
        auto original_facts_base = std::any_cast<std::vector<std::shared_ptr<Variable>>>(*fbIt->second);
        auto original_question = std::any_cast<std::shared_ptr<Variable>>(*questionIt->second);

        std::vector<double> f_times;
        std::vector<double> b_times;

        // Copy the original data
        std::vector<std::shared_ptr<Rule>> rules = original_rules;
        std::vector<std::shared_ptr<Variable>> facts_base = original_facts_base;
        std::shared_ptr<Variable> question = original_question;


        for (int i = 0; i < repeat; ++i) {
            
            reset_state(rules, facts_base,question);
            std::deque fb_q = forward_pre_processing_queue(facts_base,rules);
            
            auto start = std::chrono::high_resolution_clock::now();
            forward_algorithm_queue(fb_q,question);
            auto end = std::chrono::high_resolution_clock::now();
            
            std::chrono::duration<double> duration = end - start;
            f_times.push_back(duration.count());

        }

        double average_time = std::accumulate(f_times.begin(), f_times.end(), 0.0) / f_times.size();
        forward_execution_times.push_back({n, average_time});


        for (int i = 0; i < repeat; ++i) {
            
            reset_state(rules, facts_base,question);
            backward_pre_processing(rules, facts_base);
            
            auto start = std::chrono::high_resolution_clock::now();
            backward_algorithm(question); // change the name
            auto end = std::chrono::high_resolution_clock::now();
            
            std::chrono::duration<double> duration = end - start;
            b_times.push_back(duration.count());
        
        }

        average_time = std::accumulate(b_times.begin(), b_times.end(), 0.0) / b_times.size();
        backward_execution_times.push_back({n, average_time});

            
            
                 
    }

    return {forward_execution_times,backward_execution_times};
        
}


std::pair< std::vector<std::pair<int, double>>,std::vector<std::pair<int, double>> > measure_both_preprocessing_time(int num_bench, int k, const std::vector<int>& sizes, int repeat) {
    
    std::vector<std::pair<int, double>> forward_execution_times;
    std::vector<std::pair<int, double>> backward_execution_times;

    for (int n : sizes) {

        std::cout << "Processing size : " << n << "\n";
        
        // Generate the data using generate_benchmark
        
        std::unordered_map<std::string, std::shared_ptr<std::any>> data;
        switch (num_bench){
            case 3:
                data = generate_benchmark_worst(num_bench,n,0);
                break;
            case 4:
                data = generate_benchmark(num_bench,n,0);
                break;
            default:
                data = generate_benchmark(num_bench,k,n);


        }
        
        auto processed_data = create_set(data);

        // Retrieve the processed data
        auto rulesIt = processed_data.find("rules");
        auto fbIt = processed_data.find("facts base");
        auto questionIt = processed_data.find("question");

        if (rulesIt == processed_data.end() || fbIt == processed_data.end() || questionIt == processed_data.end()) {
            throw std::runtime_error("Processed data is missing required keys");
        }

        auto original_rules = std::any_cast<std::vector<std::shared_ptr<Rule>>>(*rulesIt->second);
        auto original_facts_base = std::any_cast<std::vector<std::shared_ptr<Variable>>>(*fbIt->second);
        auto original_question = std::any_cast<std::shared_ptr<Variable>>(*questionIt->second);

        std::vector<double> f_times;
        std::vector<double> b_times;

        // Deep copy the original data
        std::vector<std::shared_ptr<Rule>> rules = original_rules;
        std::vector<std::shared_ptr<Variable>> facts_base = original_facts_base;
        std::shared_ptr<Variable> question = original_question;


        for (int i = 0; i < repeat; ++i) {
            
            reset_state(rules, facts_base,question);
            
            
            auto start = std::chrono::high_resolution_clock::now();
            std::deque fb_q = forward_pre_processing_queue(facts_base,rules);
            auto end = std::chrono::high_resolution_clock::now();
            
            std::chrono::duration<double> duration = end - start;
            f_times.push_back(duration.count());

        }

        double average_time = std::accumulate(f_times.begin(), f_times.end(), 0.0) / f_times.size();
        forward_execution_times.push_back({n, average_time});


        for (int i = 0; i < repeat; ++i) {
            
            reset_state(rules, facts_base,question);
            
            auto start = std::chrono::high_resolution_clock::now();
            backward_pre_processing(rules, facts_base);
            auto end = std::chrono::high_resolution_clock::now();
            
            std::chrono::duration<double> duration = end - start;
            b_times.push_back(duration.count());
        
        }

        average_time = std::accumulate(b_times.begin(), b_times.end(), 0.0) / b_times.size();
        backward_execution_times.push_back({n, average_time});

            
            
                 
    }

    return {forward_execution_times,backward_execution_times};
        
}



std::vector<int> generate_sizes(int start, int end, int step) {
    std::vector<int> sizes;
    for (int i = start; i <= end; i += step) {
        sizes.push_back(i);
    }
    return sizes;
}


void save_execution_times_to_csv(const std::vector<std::pair<int, double>>& execution_times, const std::string& filename) {
    
     std::string filePath = "../csv_curves/" + filename;
    std::ofstream file(filePath);

    if (file.is_open()) {
        // Write header
        file << "Size,Time\n";

        // Write data
        for (const auto& [size, time] : execution_times) {
            file << size << "," << time << "\n";
        }

        file.close();
    } else {
        std::cerr << "Error: Unable to open file for writing\n";
    }
}




int main(int argc, char* argv[]) {
    // Check if the correct number of arguments are provided
    if (argc != 7) {
        std::cerr << "Usage: " << argv[0] << " <num_bench> <k> <end> <step> <rep> <algorithm>\n";
        std::cerr << "       <algorithm>: 'forward', 'backward', or 'both'\n";
        return 1;
    }

    // Parse command-line arguments
    int num_bench = std::atoi(argv[1]);
    int k = std::atoi(argv[2]);
    int end = std::atoi(argv[3]); 
    int step = std::atoi(argv[4]);
    int repeat = std::atoi(argv[5]);
    std::string algorithm = argv[6];

    int start = 1;

    std::vector<int> sizes = generate_sizes(start, end, step);

    if (algorithm == "forward") {
        auto f_exec_times = measure_execution_time("forward", num_bench, k, sizes, repeat);
        std::string f_filename = "forwardb" + std::to_string(num_bench) + "k" + std::to_string(k) +
                                 "n" + std::to_string(end) + "p" + std::to_string(step) + 
                                 "r" + std::to_string(repeat) + ".csv";
        std::cout << "Generated file name: " << f_filename << std::endl;
        save_execution_times_to_csv(f_exec_times, f_filename);
    } 
    
    else if (algorithm == "backward") {
        auto b_exec_times = measure_execution_time("backward", num_bench, k, sizes, repeat);
        std::string b_filename = "backwardb" + std::to_string(num_bench) + "k" + std::to_string(k) +
                                 "n" + std::to_string(end) + "p" + std::to_string(step) + 
                                 "r" + std::to_string(repeat) + ".csv";
        std::cout << "Generated file name: " << b_filename << std::endl;
        save_execution_times_to_csv(b_exec_times, b_filename);
    } 
    
    else if (algorithm == "both") {
        auto [f_exec_times, b_exec_times] = measure_both_execution_time(num_bench, k, sizes, repeat);
        
        std::string f_filename = "forwardb" + std::to_string(num_bench) + "k" + std::to_string(k) +
                                 "n" + std::to_string(end) + "p" + std::to_string(step) + 
                                 "r" + std::to_string(repeat) + ".csv";
        std::string b_filename = "backwardb" + std::to_string(num_bench) + "k" + std::to_string(k) +
                                 "n" + std::to_string(end) + "p" + std::to_string(step) + 
                                 "r" + std::to_string(repeat) + ".csv";

        std::cout << "Generated file names: " << f_filename << " and " << b_filename << std::endl;

        save_execution_times_to_csv(f_exec_times, f_filename);
        save_execution_times_to_csv(b_exec_times, b_filename);
    } 
    
    else {
        std::cerr << "Invalid algorithm specified. Use 'forward', 'backward', or 'both'.\n";
        return 1;
    }

    return 0;
}
