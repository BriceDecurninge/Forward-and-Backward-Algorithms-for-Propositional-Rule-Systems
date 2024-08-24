import re
import classes
import gc
import os
import json

from algorithms import forwardV3 as forward
from algorithms import backwardV5 as backward

from benchmarks import benchmark1 as b1
from benchmarks import benchmark2 as b2
from benchmarks import benchmark3 as b3
from benchmarks import benchmark4 as b4
from benchmarks import benchmark5 as b5

relative_path = "compare/data/"
data_path = os.path.join(os.getcwd(), relative_path)



'''
Descritpion : extracts a numeric suffix from the name of a given module. 
It uses a regular expression to find and return the digits at the end of the module's name.

Input : "module", A module object. This is a reference to an imported Python module.
Output : string representing the numeric suffix at the end of the module's name if it exists.
         None if there is no digit at the end of the module's name

Example : get_module_number(benchmark5) returns "5"

'''
def get_module_number(module):
    module_name = module.__name__
    match = re.search(r'\d+$', module_name)
    if match:
        return match.group()
    else:
        return None
    

def get_module(benchmark_name):
    if benchmark_name == 'b1' or benchmark_name == 'benchmark1':
        return b1
    elif benchmark_name == 'b2' or benchmark_name == 'benchmark2':
        return b2
    elif benchmark_name == 'b3' or benchmark_name == 'benchmark3':
        return b3
    elif benchmark_name == 'b4' or benchmark_name == 'benchmark4':
        return b4
    elif benchmark_name == 'b5' or benchmark_name == 'benchmark5':
        return b5
    else:
        raise ValueError(f"Benchmark inconnu: {benchmark_name}")

def get_algorithm(alg_name):
    if alg_name == 'forward':
        return forward
    elif alg_name == 'backward':
        return backward
    else:
        raise ValueError(f"Algorithme inconnu: {alg_name}")

'''
    Descritpion : Load benchmark data from a specified benchmark module.
                  Data is loaded from a JSON file
    Input:
        benchmark: A module object representing the benchmark.

    Returns:
        A tuple containing:
        - R: The rules extracted from the benchmark data.
        - FB: The facts base extracted from the benchmark data.
        - Q: The question extracted from the benchmark data.
    
    Example:
        >>> import benchmark1
        >>> R, FB, Q = loadBenchmark(benchmark1)
'''
def load_benchmark(benchmark) :
    path_b = "benchmark" + get_module_number(benchmark) +"/" + "bench0.json"
    where = data_path + path_b 
    
    with open(where) as myFile :
        data = json.load(myFile)
    myFile.close()
   

    for elem in data :
        objet = classes.createSet(elem)
        R = objet['rules']
        FB = objet['facts base']
        Q = objet['question']
    
    del data
    gc.collect()

    return R,FB,Q

'''
    Descritpion : Load benchmark data from a specified benchmark module.
                  Data is loaded from python dictionary and not a JSON file
    Input:
        benchmark: A module object representing the benchmark.

    Returns:
        A tuple containing:
        - R: The rules extracted from the benchmark data.
        - FB: The facts base extracted from the benchmark data.
        - Q: The question extracted from the benchmark data.
    
    Example:
        >>> import benchmark1
        >>> R, FB, Q = loadBenchmark(benchmark1)
'''

def load_benchmark2(data) :
   
    objet = classes.createSet2(data)
    R = objet['rules']
    FB = objet['facts base']
    Q = objet['question']

    return R,FB,Q