'''
Description : This file provides a series of functions that
helps testing different implementations of forward and backward
algorithms
'''
####################IMPORTS#####################################


# Enable faulthandler to dump the Python traceback on a crash to a file
#with open('traceback.log', 'w') as f:
    #faulthandler.enable(file=f)

from io import StringIO
import os
import timeit as timeit
import sys
import numpy as np

import backwardV5 as backward
import forwardV3 as forward

import benchmark1 as b1
import benchmark2 as b2
import benchmark3 as b3
import benchmark4 as b4
import benchmark5 as b5

import time_measuring
import load_data

import cProfile
import pstats
import time
from time import perf_counter
import objgraph
import copy

path = "/home/ecyrbe/Desktop/implem/compare/"

import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(500000)

# Relative path to the data directory
relative_path = "compare/tests/"


# Get the absolute path based on the current working directory
data_path = os.path.join(os.getcwd(), relative_path)

print("Data path:", data_path)

'''
Description : Test the forwardalgorithm V3 (linear) on a benchmark
Prints to see if algorithm behave well meaning :
- facts must have rules in variable.rules
- facts must reference same object as antecedents rules
- forwardalgorithmV3 must return true
'''

# Not working needs to be change
def test_forward(benchmark) :
    
    data = benchmark.create_benchmark2(k=9,n=4,show=True)
    rules,facts_base,question = load_data.loadBenchmark2(set)
    
    #R,FB,Q = chargeBenchmark(benchmark,k=4,n=9)

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
    if (forward.forwardAlgorithmSteps3(FB,R,Q)) :
        print ("output : true")

#faulthandler.enable(all_threads=True)
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
    #pdb.set_trace()
    if (backward.main(question)) :
        print ("output : true")


def testNoJson(bench,k,size):
    set = bench.create_benchmark2(k,size,True)
    R,FB,Q = load_data.loadBenchmark2(set)
    forward.FordwardAlgorithmSteps3(FB,R,Q)


#testNoJson(b1,9,4)
#testforw3(b1)


relative_path = "compare/data/"


# Get the absolute path based on the current working directory
data_path = os.path.join(os.getcwd(), relative_path)



def checkSpeed(exec_timef,exec_timeb,k):
    
    # Calculate the average execution times
    avg_time_f = sum(exec_timef) / len(exec_timef)
    avg_time_b = sum(exec_timeb) / len(exec_timeb)

    # Compute the speedup factor
    speedup_factor = avg_time_f / avg_time_b

    # Desired speedup factor
    

    # Print the results
    print(f"Average execution time of forward: {avg_time_f:.6f} seconds")
    print(f"Average execution time of backward: {avg_time_b:.6f} seconds")
    print(f"Computed speedup factor: {speedup_factor:.2f}")

    # Check if Algorithm 1 is approximately k times faster than Algorithm 2
    if abs(speedup_factor - k) < 0.1:  # Allowing a small tolerance for floating-point comparison
        print(f"Algorithm 1 is approximately {k} times faster than Algorithm 2.")
    else:
        print(f"Algorithm 1 is not {k} times faster than Algorithm 2.")


def test_pre_proc(algorithm,benchmark,repeat,k,sizes):
    exec_time=[]

    for size in sizes:
        print ("processing size " + str(size))
        data = benchmark.create_benchmark2(k=k,n=size,show=False)
        rules,facts_base,_ = load_data.load_benchmark2(data)

        time = time_measuring.time_pre_processing(algorithm,rules=rules,facts_base=facts_base,repeat=repeat)
        print(time)
        exec_time.append(time)

    return exec_time

'''
executes forward preprocessing on a facts_base and a list of rules a repeat number of times.
Output : the average execution time and the execution time of the first iterations

'''
def test_pre_proc0a(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, initial_question = load_data.load_benchmark2(data)
    
    
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




# Measuring pre_processing without function call
def test_pre_proc0b(benchmark, k, n, repeat) :
    
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, _ = load_data.load_benchmark2(data)
    
    
    exec_time = []
    mean_time = 0.

    for _ in range (repeat) :
        
        rules = copy.deepcopy(initial_rules)
        facts_base = copy.deepcopy(initial_facts_base)
        
        start_time = time.time()
        
        for rule in rules :
            for antecedent in rule.antecedents :
                rule.counter += 1
                #antecedent.addRule(rule)
        for variable in facts_base :
            variable.value=True

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

# Profiling pre_processing
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


# Measures time for pre_processing a repeat number of times
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")


# Measures time for pre_processing a repeat number of times with perf counter
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")

def test_pre_proc1(facts_base, rules):
    pr = cProfile.Profile()
    pr.enable()

# Measures time for pre_processing a repeat number of times with perf counter
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")


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

def test_pre_proc1(facts_base, rules):
    pr = cProfile.Profile()
    pr.enable()

    # Profile processing rules and antecedents
    for rule in rules:
        for antecedent in rule.antecedents:
            rule.counter += 1
            # Log statement to understand the loop
            # print(f"Processing antecedent {antecedent} for rule {rule}")

    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling rules and antecedents in pre_processing:")
    ps.print_stats()
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()

    # Profile processing facts base
    for variable in facts_base:
        variable.value = True

    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling facts base in pre_processing:")
    ps.print_stats()
    print(s.getvalue())


def test_pre_proc2(facts_base, rules):
    # Profile processing rules and antecedents
    start_time = time.time()
    rule_iterations = 0
    antecedent_iterations = 0

    for rule in rules:
        rule_iterations += 1
        for antecedent in rule.antecedents:
            antecedent_iterations += 1
            rule.counter += 1
            antecedent.addRule(rule)
    end_time = time.time()
    print(f"Time taken for processing rules and antecedents: {end_time - start_time} seconds")
    print(f"Number of rule iterations: {rule_iterations}")
    print(f"Number of antecedent iterations: {antecedent_iterations}")

    # Profile processing facts base
    start_time = time.time()
    facts_base_iterations = 0

    for variable in facts_base:
        facts_base_iterations += 1
        variable.value = True
    end_time = time.time()
    print(f"Time taken for processing facts base: {end_time - start_time} seconds")
    print(f"Number of facts base iterations: {facts_base_iterations}")


def test_pre_proc3(facts_base, rules):

    for rule in rules :
        for antecedent in rule.antecedents :
            rule.counter += 1
            antecedent.addRule(rule)
    for variable in facts_base :
        variable.value=True

    
    output_path = data_path + "/object_graph.png"

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Visualize object references
    
    #objgraph.show_refs([facts_base[0]], filename=output_path)
    objgraph.show_refs([rules[0]], filename=output_path, max_depth=3, refcounts=True, extra_info=lambda x: "size: {}".format(sys.getsizeof(x)))



def test_pre_proc4(facts_base, rules):
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


def test_forward0c(benchmark, k, n, repeat) :
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    initial_rules, initial_facts_base, initial_question = load_data.load_benchmark2(data)
    
    pr = cProfile.Profile()
    
    for _ in range (repeat) :
        
        rules = copy.deepcopy(initial_rules)
        facts_base = copy.deepcopy(initial_facts_base)
        question = copy.deepcopy(initial_question)
        
        forward.pre_processing(facts_base,rules)
        
        pr.enable()
        #forward.forward_algorithm(facts_base,question)
        result = False
        for variable in facts_base :
            if variable.used == False :
                for rule in variable.rules :
                    rule.counter -= 1
                    if rule.counter == 0 :
                        if rule.consequent.name == question.name :
                            result = True
                            break
                        facts_base.append(rule.consequent)
                variable.used = True
                if result:
                    break
        
        pr.disable()
       
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue()) 


def test_forward0d(benchmark, k, n, repeat) :
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    pr = cProfile.Profile()
    
    for _ in range (repeat) :
        
        rules,facts_base,question = load_data.load_benchmark2(data)
        
        forward.pre_processing(facts_base,rules)
        
        pr.enable()
        forward.forward_algorithm(facts_base,question)
        '''
         result = False
        for variable in facts_base :
            if variable.used == False :
                for rule in variable.rules :
                    rule.counter -= 1
                    if rule.counter == 0 :
                        if rule.consequent.name == question.name :
                            result = True
                            break
                        facts_base.append(rule.consequent)
                variable.used = True
                if result:
                    break
        
        '''
       
        pr.disable()
       
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("Profiling forward_algorithm:")
    ps.print_stats()
    print(s.getvalue()) 

# Process forward algorith a repeat number of time and returns the average execution time
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")

# Like test_forward0f but used perf_count instead of time
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")


# Process forward algorith a repeat number of time and returns the average execution time
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")

# Like test_backward0f but used timeit.default_counter() instead of time
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

    # Print the first 20 elements of exec_time in scientific notation
    print("First 20 execution times in scientific notation:")
    for elapsed in exec_time[:20]:
        print(f"{elapsed:.4e}")


def test_backward0d(benchmark, k, n, repeat) :
   
    data = benchmark.create_benchmark2(k=k,n=n,show=False)
    
    pr = cProfile.Profile()
    
    for _ in range (repeat) :
        
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

def test_forward2(facts_base, question):
    start_time = time.time()
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
                        end_time = time.time()
                        print(f"Total time taken: {end_time - start_time} seconds")
                        print(f"Number of variable iterations: {variable_iterations}")
                        print(f"Number of rule iterations: {rule_iterations}")
                        return True
                    facts_base.append(rule.consequent)
            variable.used = True

    print(str(len(facts_base)))
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")
    print(f"Number of variable iterations: {variable_iterations}")
    print(f"Number of rule iterations: {rule_iterations}")
    
    return False


    




def main():
    if len(sys.argv) != 7:
        print("Usage: python drawGraph.py <alg> <benchmark> <k> <max> <step> <rep>")
        sys.exit(1)

    alg_name = sys.argv[1]
    benchmark_name = sys.argv[2]
    k = int(sys.argv[3])
    size_max = int(sys.argv[4])
    step = int(sys.argv[5])
    repetitions = int(sys.argv[6])

    # Définir les tailles en fonction des arguments
    sizes = np.arange(1, size_max, step)
    
    # Sélectionner l'algorithme à utiliser
    algorithm = load_data.get_algorithm(alg_name=alg_name)
    # Sélectionner le benchmark à utiliser
    benchmark_module = load_data.get_module(benchmark_name=benchmark_name)

    # Exécuter l'algorithme et mesurer le temps d'exécution
    #exec_time = timeAlgorithm2(algorithm=algorithm, benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions, both=False)
    #time_measuring.drawLinear(alg_name, benchmark_name,sizes, exec_time, both=False)
    #exec_time_f = timeAlgorithm2(algorithm=forward, benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions, both=False)
    #exec_time_b = timeAlgorithm2(algorithm=backward, benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions, both=False)
    
    #checkSpeed(exec_timef=exec_time_f,exec_timeb=exec_time_b,k=k)
    # Dessiner le graphique
    #time_measuring.drawLinear(alg_name, benchmark_name,sizes, exec_time, both=False)

    '''
      pr = cProfile.Profile()
    pr.enable()
    
  
      pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    '''
  

    #exec_timep = test_pre_proc(algorithm=algorithm,benchmark=benchmark_module,repeat=repetitions,k=k,sizes=sizes)
    #exec_timea = time_measuring.time_algorithm2(algorithm=algorithm, benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions)
    '''
     pr = cProfile.Profile()
    pr.enable()
    
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    '''
   
    
    #time_measuring.draw_graph("backward","b1",sizes,execution_time=exec_time,both=False)
    #time_measuring.draw_both(benchmark_name,sizes,exec_timea,exec_timep)

    #exec_timep, exec_timea = time_measuring.time_phases(algorithm=algorithm,benchmark=benchmark_module,sizes=sizes,k=k,repeat=repetitions)

    #time_measuring.draw_phases(alg_name=alg_name,bench_name=benchmark_name,sizes=sizes,exec_timep=exec_timep,exec_timea=exec_timea)

    
    '''
     data = benchmark_module.create_benchmark2(k=k,n=5000,show=False)
    rules,facts_base,question = load_data.load_benchmark2(data)
    
    #for size in sizes:
        #test_pre_proc2(facts_base=facts_base,rules=rules)
        #forward.pre_processing(facts_base=facts_base,rules=rules)
        #test_forward2(facts_base=facts_base,question=question)
    
    #test_pre_proc4(facts_base=facts_base,rules=rules)

    backward.pre_processing(rules=rules,facts_base=facts_base)
   
    
    size_tracker = backward.SizeTracker()

    backward.test_main(Q=question,size_tracker=size_tracker)

    print (size_tracker.get_cumulative_size())

    '''
   


    '''
    # Create some objects
    a = [1, 2, 3]
    b = {'x': 1, 'y': 2}
    c = (a, b)

    output_path = data_path + "/object_graph.png"

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Visualize object references
    objgraph.show_refs([c], filename=output_path)

    # Display top N objects by size
    objgraph.show_most_common_types(limit=10)

    '''



    exec_timep, exec_timea = time_measuring.time_phases(algorithm=algorithm,benchmark=benchmark_module,sizes=sizes,k=k,repeat=repetitions)

    time_measuring.draw_phases(alg_name=alg_name,bench_name=benchmark_name,sizes=sizes,exec_timep=exec_timep,exec_timea=exec_timea)

        

if __name__ == "__main__":
    #testback3(b1)
    #main()
    #test_pre_proc0b(b1,5,5000,200)
    #test_back_pre_proc0d(b1,5,10000,200)
    #testback3(b1)
    data = b1.create_benchmark2(k=5,n=10000,show=False)
    rules,facts_base,question = load_data.load_benchmark2(data)
    forward.pre_processing(facts_base,rules)
    test_forward2(facts_base,question)
    #exec_timep, exec_timea = time_measuring.time_phases(algorithm=algorithm,benchmark=benchmark_module,sizes=sizes,k=k,repeat=repetitions)

    #time_measuring.draw_phases(alg_name=alg_name,bench_name=benchmark_name,sizes=sizes,exec_timep=exec_timep,exec_timea=exec_timea)
