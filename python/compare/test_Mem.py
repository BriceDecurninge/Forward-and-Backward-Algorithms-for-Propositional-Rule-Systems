
import sys
import os
import numpy as np

from benchmarks import benchmark1 as b1
from benchmarks import benchmark2 as b2
from benchmarks import benchmark3 as b3
from benchmarks import benchmark4 as b4
from benchmarks import benchmark5 as b5

from algorithms import forwardV3 as forward
from algorithms import backwardV5 as backward

from memory_profiler import profile
import cProfile
import pstats
import timeit

import load_data


relative_path = "compare/data/"
data_path = os.path.join(os.getcwd(), relative_path)


@profile
def test_create(benchmark,size,k,both):
    for _ in [size] :
        if both:
            benchmark.create_benchmark(n=size, k=size)
        elif (benchmark == b1 or benchmark == b2 or benchmark == b5) :
            benchmark.create_benchmark(n=size, k=k)
        else:
            benchmark.create_benchmark(k=size)


@profile
def test_create2(benchmark,size,k):
   
    benchmark.create_benchmark2(n=size, k=k,show=False)
        

@profile
def time_mem(algorithm, benchmark, sizes, k, repeat): 
    execution_time = []


    for size in sizes:
        
        print("processing with size " + str(size))

        data = benchmark.create_benchmark2(k,size,False)
        rules,facts_base,question = load_data.loadBenchmark2(data)
        

        if algorithm == forward:
            forward.pre_processing(facts_base,rules)
            timer = timeit.timeit(lambda: forward.forward_algorithm(facts_base,rules, question), number=repeat)
        
        elif algorithm == backward:
            algorithm.preTreatment(rules, facts_base)
            timer = timeit.timeit(lambda: backward.main(question), number=repeat)

        execution_time.append(timer)


    return execution_time


def main():
    if len(sys.argv) != 8:
        print("Usage: python test_mem.py <alg> <benchmark> <k> <max> <step> <rep>")
        sys.exit(1)

    alg_name = sys.argv[1]
    benchmark_name = sys.argv[2]
    k = int(sys.argv[3])
    size_max = int(sys.argv[4])
    step = int(sys.argv[5])
    repetitions = int(sys.argv[6])

   
    sizes = np.arange(1, size_max, step)
    
    
    algorithm = load_data.get_algorithm(alg_name)
    benchmark_module = load_data.get_module(benchmark_name=benchmark_name)

    time_mem(algorithm,benchmark_module,sizes,k,repetitions)
    #test_create2(b1,1000,4)

if __name__ == "__main__":
    main()