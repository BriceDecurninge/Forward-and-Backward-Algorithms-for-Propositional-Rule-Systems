'''
Description : This file provides a series of functions that
helps testing different implementations of forward and backward
algorithms
'''


####################IMPORTS#####################################

from io import StringIO
import os
import sys
import numpy as np

#import of algortihms
from algorithms import backwardV5 as backward
from algorithms import forwardV3 as forward

#import of benchmarks
from benchmarks import benchmark1 as b1
from benchmarks import benchmark2 as b2
from benchmarks import benchmark3 as b3
from benchmarks import benchmark4 as b4
from benchmarks import benchmark5 as b5

#import of drawing and loading module
import time_measuring
import load_data

#import of time_measuring tools
import cProfile
import pstats
import time
import timeit as timeit
from time import perf_counter
import copy


import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(500000)


# Relative path to the data directory
relative_path = "compare/tests/"

# Get the absolute path based on the current working directory
data_path = os.path.join(os.getcwd(), relative_path)





'''
Description : Test the forwardalgorithm V3 (linear) on a benchmark
Prints to see if algorithm behave well meaning :
- facts must have rules in variable.rules
- facts must reference same object as antecedents rules
- forwardalgorithmV3 must return true
'''
def test_forward(benchmark) :
    
    data = benchmark.create_benchmark2(k=9,n=4,show=True)
    rules,facts_base,question = load_data.load_benchmark2(data)
    
   
    #Check if fact references same object as antecedents
    for fact in facts_base:
        for rule in rules:
            for antecedent in rule.antecedents :
                if fact is antecedent :
                    print ("fact " + fact.name + " is the same as " + antecedent.name)

    print()
    forward.pre_processing(facts_base=facts_base,rules=rules)

    for rule in rules:
        print (str(rule))
        print()

    print() 
    #check if facts know the rules they are in
    for fact in facts_base :
        print ("Nbr règles " + fact.name + " " + str(len(fact.rules)))
    
    print()
    print ("Question is " + question.name)
    print()
    print ("Execution of forward lin algorithm")
    print()

    #check if forwardlinear algorithm behave well and return true
    if (forward.forward_algorithm_steps(facts_base=facts_base,question=question)) :
        print ("output : true")



'''
Description : Test the backward algorithm on a benchmark
Prints to see if algorithm behave well meaning :
- facts must have rules in variable.rules
- facts must reference same object as antecedents rules
- backward algorithm must go through coherent path and must return true
'''
def testback3(benchmark):
    
    data = benchmark.create_benchmark2(k=5,n=10000,show=False)
    rules,facts_base,question = load_data.load_benchmark2(data)
    

    for rule in rules:
        print (str(rule))
        print()
    
    print() 
    
    #check if facts know the rules they are in
    for fact in facts_base :
        print ("Nbr règles " + fact.name + " " + str(len(fact.rules)))
    
    print()
    print ("Question is " + question.name)
    print()
    print ("Execution of backward lin algorithm")
    print()

    #check if backwardlinear algorithm behave well and return true
    backward.pre_processing(rules,facts_base)
    if (backward.main_steps(question)) :
        print ("output : true")



'''Description : Measures the speed coefficient between forward and backward algorithms'''
def check_speed(exec_timef,exec_timeb,k):
    
    # Calculate the average execution times
    avg_time_f = sum(exec_timef) / len(exec_timef)
    avg_time_b = sum(exec_timeb) / len(exec_timeb)

    # Compute the speedup factor
    speedup_factor = avg_time_f / avg_time_b


    # Print the results
    print(f"Average execution time of forward: {avg_time_f:.6f} seconds")
    print(f"Average execution time of backward: {avg_time_b:.6f} seconds")
    print(f"Computed speedup factor: {speedup_factor:.2f}")

    # Check if Algorithm 1 is approximately k times faster than Algorithm 2
    if abs(speedup_factor - k) < 0.1:  # Allowing a small tolerance for floating-point comparison
        print(f"Algorithm 1 is approximately {k} times faster than Algorithm 2.")
    else:
        print(f"Algorithm 1 is not {k} times faster than Algorithm 2.")




'''Description : Measures time for forward pre_processing a repeat number of times using deep_copy and time.time()'''
def test_pre_proc0a(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, _ = load_data.load_benchmark2(data)
    
    
    exec_time = []
    mean_time = 0.

    for _ in range (repeat) :
        
        rules = copy.deepcopy(initial_rules)
        facts_base = copy.deepcopy(initial_facts_base)
        start_time = time.time()
        forward.pre_processing(facts_base,rules)
        end_time = time.time()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")





'''Descritpion : Profiles pre_processing with deep copying '''
def test_pre_proc0c(benchmark, k, n, repeat) :
   
    pr = cProfile.Profile()
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, _ = load_data.load_benchmark2(data)
   
    
    for _ in range (repeat) :
        
        rules = copy.deepcopy(initial_rules)
        facts_base = copy.deepcopy(initial_facts_base)
        
        pr.enable()
        for rule in rules :
            for antecedent in rule.antecedents :
                rule.counter += 1
                antecedent.addRule(rule)
        for variable in facts_base :
            variable.value=True
        pr.disable()

   
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling rules forward pre_processing:")
    ps.print_stats()
    print(s.getvalue())




'''Description : Profile pre_processing without deep copying'''
def test_pre_proc0d(benchmark, k, n, repeat) :
   
    pr = cProfile.Profile()
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    for _ in range (repeat) :
        
        rules, facts_base, _ = load_data.load_benchmark2(data)
        
        pr.enable()
        forward.pre_processing(facts_base,rules)
        pr.disable()

    
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling rules forward pre_processing:")
    ps.print_stats()
    print(s.getvalue())




'''Description : Measures time for pre_processing a repeat number of times using time.time()'''
def test_pre_proc0e(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, _ = load_data.load_benchmark2(data)
        
        start_time = time.time()
        forward.pre_processing(facts_base,rules)
        end_time = time.time()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Descritpion : Measures time for pre_processing a repeat number of times with perf counter'''
def test_pre_proc0f(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, _ = load_data.load_benchmark2(data)
        
        start_time = perf_counter()
        forward.pre_processing(facts_base,rules)
        end_time = perf_counter()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Description : Measures time for pre_processing a repeat number of times with perf_counter()'''
def test_back_pre_proc0f(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, _ = load_data.load_benchmark2(data)
        
        start_time = timeit.default_timer()
        backward.pre_processing(facts_base=facts_base,rules=rules)
        end_time = timeit.default_timer()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Descritpion : Profiles backward pre_processing'''
def test_back_pre_proc0d(benchmark, k, n, repeat) :
   
    pr = cProfile.Profile()
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, _ = load_data.load_benchmark2(data)
        
        pr.enable()
        backward.pre_processing(rules,facts_base)
        pr.disable()

     
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling rules forward pre_processing:")
    ps.print_stats()
    print(s.getvalue())



'''Descritpion : shows the number of iterations of forward pre_processing'''
def test_pre_proc2(facts_base, rules):
    # Profile processing rules and antecedents
    rule_iterations = 0
    antecedent_iterations = 0

    for rule in rules:
        rule_iterations += 1
        for antecedent in rule.antecedents:
            antecedent_iterations += 1
            rule.counter += 1
            antecedent.addRule(rule)
    
    print(f"Number of rule iterations: {rule_iterations}")
    print(f"Number of antecedent iterations: {antecedent_iterations}")

    # Profile processing facts base
    facts_base_iterations = 0

    for variable in facts_base:
        facts_base_iterations += 1
        variable.value = True
    print(f"Number of facts base iterations: {facts_base_iterations}")





''' Description : Profiles forward algorithm with no repetitions'''
def test_forward(facts_base, question):
    pr = cProfile.Profile()
    pr.enable()

    for variable in facts_base:
        if not variable.used:
            for rule in variable.rules:
                rule.counter -= 1
                if rule.counter == 0:
                    if rule.consequent.name == question.name:
                        pr.disable()
                        s = StringIO()
                        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                        print("Profiling forward_algorithm:")
                        ps.print_stats()
                        print(s.getvalue())
                        return True
                    facts_base.append(rule.consequent)
            variable.used = True

    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue())
    
    return False



'''Description : Shows the number of iterations of the forward_algorithm'''
def test_forward2(facts_base, question):

    variable_iterations = 0
    rule_iterations = 0

    for variable in facts_base:
        variable_iterations += 1
        if not variable.used:
            for rule in variable.rules:
                rule_iterations += 1
                rule.counter -= 1
                if rule.counter == 0:
                    if rule.consequent.name == question.name:
                        print(f"Number of variable iterations: {variable_iterations}")
                        print(f"Number of rule iterations: {rule_iterations}")
                        return True
                    facts_base.append(rule.consequent)
            variable.used = True


    print(f"Number of variable iterations: {variable_iterations}")
    print(f"Number of rule iterations: {rule_iterations}")
    
    return False



'''Descritpion : Measures a repeat number of time the execution_time of forward algorithm using deep_copy'''
def test_forward0a(benchmark, k, n, repeat) :
     
    exec_time = []
    mean_time = 0.

    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, initial_question = load_data.load_benchmark2(data)
    

    for _ in range (repeat) :
        
        rules = copy.deepcopy(initial_rules)
        facts_base = copy.deepcopy(initial_facts_base)
        question = copy.deepcopy(initial_question)
        
        forward.pre_processing(facts_base,rules)
        
        start_time = time.time()
        forward.forward_algorithm(facts_base,question)
        end_time = time.time()

        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)
   
    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")




''' Description : Test if timeit measures the time correctly for forward algorithm'''
def test_forward0b(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    rules, facts_base,question = load_data.load_benchmark2(data)
    forward.pre_processing(facts_base,rules)

    pr = cProfile.Profile()
    pr.enable()

    timeit.timeit(lambda facts_base=facts_base,question=question: forward.forward_algorithm(facts_base,question), number=repeat)

    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue())



'''Descriptipn : Profiles forwars algorithm'''
def test_forward0d(benchmark, k, n, repeat) :
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    pr = cProfile.Profile()
    
    for _ in range (repeat) :
        
        rules,facts_base,question = load_data.load_benchmark2(data)
        
        forward.pre_processing(facts_base,rules)
        
        pr.enable()
        forward.forward_algorithm(facts_base,question)   
        pr.disable()
       
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue()) 



'''Description : Measures time for forward_algorithm a repeat number of times using time.time()'''
def test_forward0e(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, question = load_data.load_benchmark2(data)
        forward.pre_processing(facts_base,rules)
        
        start_time = time.time()
        forward.forward_algorithm(facts_base,question)
        end_time = time.time()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Description : Measures time for forward_algorithm a repeat number of times using perf_counter()'''
def test_forward0f(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, question = load_data.load_benchmark2(data)
        forward.pre_processing(facts_base,rules)
        
        start_time = perf_counter()
        forward.forward_algorithm(facts_base,question)
        end_time = perf_counter()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Descritpion : Profiles backward algorithm'''
def test_backward0d(benchmark, k, n, repeat) :
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    pr = cProfile.Profile()
    
    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))
        rules,facts_base,question = load_data.load_benchmark2(data)
        
        backward.pre_processing(rules,facts_base)
        
        pr.enable()
        backward.main(question)
        pr.disable()
       
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue()) 



'''Description : Measures time for backward_algorithm a repeat number of times using time.time()'''
def test_backward0e(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, question = load_data.load_benchmark2(data)
        backward.pre_processing(facts_base=facts_base,rules=rules)
        
        start_time = time.time()
        backward.main(question)
        end_time = time.time()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")




'''Description : Measures time for backward_algorithm a repeat number of times using timeit.default_time()'''
def test_backward0f(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
   
    
    exec_time = []
    mean_time = 0.

    for i in range (repeat) :
        
        print ("Processing iteration n " + str(i))

        rules, facts_base, question = load_data.load_benchmark2(data)
        backward.pre_processing(facts_base=facts_base,rules=rules)
        
        start_time = timeit.default_timer()
        backward.main(question)
        end_time = timeit.default_timer()


        elapsed_time = end_time - start_time
        mean_time += elapsed_time
        exec_time.append(elapsed_time)

    mean_time /= repeat
    
    print(f"Mean execution time: {mean_time:.4e} seconds")
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")



'''Description : Shows the memory size of list of rules, list of variables, rule and variable'''
def measure_sizes(facts_base, rules):
    # Calculate size of rules list
    size_rules = sys.getsizeof(rules)

    # Calculate size of facts_base list
    size_facts_base = sys.getsizeof(facts_base)

    # Calculate size of one fact in facts_base
    if facts_base:
        size_one_fact = sys.getsizeof(facts_base[0])
    else:
        size_one_fact = 0

    # Calculate size of one rule object
    if rules:
        size_one_rule = sys.getsizeof(rules[0])
    else:
        size_one_rule = 0

    # Calculate size of antecedents
    antecedents = []
    for rule in rules:
        antecedents.extend(rule.antecedents)
    size_antecedents = sum(sys.getsizeof(antecedent) for antecedent in antecedents)

    # Print sizes
    print(f"Size of rules list: {size_rules} bytes")
    print(f"Size of facts_base list: {size_facts_base} bytes")
    print(f"Size of one fact in facts_base: {size_one_fact} bytes")
    print(f"Size of one rule object: {size_one_rule} bytes")
    print(f"Size of antecedents: {size_antecedents} bytes")



def test_generate_and_process_benchmark(facts_base,rules,question):
    # Pre-process the data using backward_pre_processing
    # Run the main algorithm on the question variable
    #backward.main_steps(question)
    forward.forward_algorithm(facts_base=facts_base,question=question)
    # Print the result


def reset_state(rules, facts_base, question):
    for rule in rules:
        rule.reset()
        for antecedent in rule.antecedents:
            antecedent.reset_ant()
        if rule.consequent:
            #print("je reset consequent")
            rule.consequent.reset()
    
    for variable in facts_base:
        variable.reset()
    
    if question:
        #print("je reset question")
        question.reset_ant()

def measure_execution_time(benchmark, k, sizes, repeat):
    execution_times = []

    for n in sizes:
        print ("processing size " + str(n) + "\n")
        data = benchmark.create_benchmark2(k=k,n=n,show=False)
        rules, facts_base, question = load_data.load_benchmark2(data)
        
       
        times = []

        for _ in range(repeat):
            # Deep copy the original data (assume copy.deepcopy works as expected)
            
            reset_state(rules, facts_base, question)
            
            forward.pre_processing(facts_base=facts_base,rules=rules)

            start_time = time.time()
            test_generate_and_process_benchmark(facts_base,rules,question)
            end_time = time.time()

            duration = end_time - start_time
            times.append(duration)

        average_time = np.mean(times)
        execution_times.append((n, average_time))

    return execution_times




def main():
    if len(sys.argv) != 7:
        print("Usage: python test.py <alg> <benchmark> <k> <max> <step> <rep>")
        sys.exit(1)

    alg_name = sys.argv[1]
    benchmark_name = sys.argv[2]
    k = int(sys.argv[3])
    size_max = int(sys.argv[4])
    step = int(sys.argv[5])
    repetitions = int(sys.argv[6])

    # Defining the sizes
    sizes = np.arange(1, size_max, step)
    
    # Selecting the algorithm
    algorithm = load_data.get_algorithm(alg_name=alg_name)
    
    # Selecting the benchmark
    benchmark_module = load_data.get_module(benchmark_name=benchmark_name)


    # Drawing of phases executions time
    exec_timep, exec_timea = time_measuring.time_phases(algorithm=algorithm,benchmark=benchmark_module,sizes=sizes,k=k,repeat=repetitions)

    time_measuring.draw_phases(alg_name=alg_name,bench_name=benchmark_name,sizes=sizes,exec_timep=exec_timep,exec_timea=exec_timea)

import pandas as pd   

if __name__ == "__main__":
    #main()

    num_bench = 1
    k = 5
    step = 50
    size_max = 5000
    sizes = np.arange(1, size_max, step)
    repeat = 200
    oriented = False
    execution_times = measure_execution_time(b1, k, sizes, repeat)

    # Save results to CSV
    df = pd.DataFrame(execution_times, columns=["Size", "Time"])
    df.to_csv("python_execution_times.csv", index=False)
   

        