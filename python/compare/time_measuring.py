'''
Author : Brice Decurninge

Description : This file includes different functions
enabling to draw graphs of the execution time of Horn SAT solver
algorithms on different benchmarks
'''
import time
import numpy as np
import copy

import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))

import pandas as pd

from algorithms import backwardV5 as backward
from algorithms import forwardV3 as forward

from benchmarks import benchmark1 
from benchmarks import benchmark2 
from benchmarks import benchmark3 
from benchmarks import benchmark4 
from benchmarks import benchmark5 

import timeit as timeit


import numpy as np
import os

import sys
sys.setrecursionlimit(1000000)

import load_data



# Relative path to the data directory
relative_path = "compare/data/"


# Get the absolute path based on the current working directory
data_path = os.path.join(os.getcwd(), relative_path)



def reset_state(rules, facts_base, question):
    for rule in rules:
        rule.reset()
        for antecedent in rule.antecedents:
            antecedent.reset()
        if rule.consequent:
            rule.consequent.reset()
    
    for variable in facts_base:
        variable.reset()

    if question:
        question.reset()


def measure_execution_time(benchmark, alg, k, sizes, repeat):
    execution_times = []

    for n in sizes:
        print(f"Processing size: {n}\n")
        
        # Generate benchmark data
        data = benchmark1.create_benchmark2(k=k, n=n, show=False)
        rules, facts_base, question = load_data.load_benchmark2(data)

        
        times = []

        for _ in range(repeat):
            if rules is None or facts_base is None or question is None:
                raise ValueError("Failed to load rules, facts_base, or question from benchmark data.")
            # Ensure none of them are None
            
            # Reset the state before each run
            reset_state(rules, facts_base, question)
            

            if alg == "forward":
                facts_base = forward.pre_processing(facts_base, rules)

                start_time = time.time()
                forward.forward_algorithm (facts_base, question)
                end_time = time.time()

            elif alg == "backward":
                backward.pre_processing(rules, facts_base)

                start_time = time.time()
                backward.main(question)
                end_time = time.time()

            else:
                raise ValueError("Algorithm can be either 'forward' or 'backward'")

            duration = end_time - start_time
            times.append(duration)

        average_time = np.mean(times)
        execution_times.append((n, average_time))

    return execution_times



def time_pre_processing(algorithm,rules,facts_base,repeat) :
    timer = timeit.timeit(lambda:algorithm.pre_processing(facts_base=facts_base,rules=rules) , number=repeat)
    return timer



def save_execution_times_to_csv(execution_times, filename):
    """
    Save execution times to a CSV file.

    Parameters:
    execution_times (list of tuples): A list containing tuples of (size, time).
    filename (str): The filename to save the CSV as.
    """
    df = pd.DataFrame(execution_times, columns=['Size', 'Time'])
    df.to_csv(filename, index=False)
    print(f"Execution times saved to {filename}")

def main():
    if len(sys.argv) != 8:
        print("Usage: python drawGraph.py <alg> <benchmark> <k> <max> <step> <rep> <both>")
        sys.exit(1)

    alg_name = sys.argv[1]
    benchmark_name = sys.argv[2]
    k = int(sys.argv[3])
    size_max = int(sys.argv[4])
    step = int(sys.argv[5])
    repetitions = int(sys.argv[6])
    both = sys.argv[7].lower() == "true"
   
    sizes = np.arange(1, size_max + 1, step)
    

    # Selecting the benchmark
    benchmark_module = load_data.get_module(benchmark_name)

    if both:
        exec_timef = measure_execution_time(alg="forward", benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions)
        exec_timeb = measure_execution_time(alg="backward", benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions)

        # Generate filenames for both forward and backward execution times
        f_filename = f"forwardb{benchmark_name}k{k}n{size_max}p{step}r{repetitions}.csv"
        b_filename = f"backwardb{benchmark_name}k{k}n{size_max}p{step}r{repetitions}.csv"

        # Save to CSV
        save_execution_times_to_csv(exec_timef, f_filename)
        save_execution_times_to_csv(exec_timeb, b_filename)

    else:
        # Execute the algorithm and measure the execution time
        exec_time = measure_execution_time(alg=alg_name, benchmark=benchmark_module, sizes=sizes, k=k, repeat=repetitions)
        
        # Generate filename based on the algorithm name
        filename = f"{alg_name}b{benchmark_name}k{k}n{size_max}p{step}r{repetitions}.csv"

        # Save to CSV
        save_execution_times_to_csv(exec_time, filename)

if __name__ == "__main__":
    main()

