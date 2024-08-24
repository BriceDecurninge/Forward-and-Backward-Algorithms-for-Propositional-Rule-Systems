
27/06
Timeit does not take the same initial input over the repetitions.
It means that if mutable objects are modified throughout the process; next iteration will use the modified objects and not the orginal versions of them.

That is why in order to perform multiple iterations, it is necessary to initialise the objects : facts_base, rules, and question before every iteration.

Example :

for _ in range (repeat) :
        
        rules,facts_base,question = load_data.load_benchmark2(data)
        
        start_time = time.time()
        forward.pre_processing(facts_base,rules)
        end_time = time.time()

        elapsed_time = end_time - start_time

01/06

Remind that if a file requires multiple files, every file needs to be compiled.


I printed some characteristics of forward pre_processing and it seems right.
Variable seems to know their rules and rules counter seem well initialized.

Issue was found on forward algorithm. In c++, if a container needs to be reallocated, it can get the iterators obsolete (see C++ document).
Every time we add a Variable on the vector facts_base, the vector is reallocated somewhere else in memory which corrupt the iterators.
To patch this, a while loop using indexes was used (see C++ document).

The new version using while loop still presented a strange segfault error.
variable->use(); This line triggered segfault error, the memory adresse could not be accessed.
It was solved by using a validity test before :  
            if (variable) {  // Ensure variable is still valid
                variable->used = true;  // Mark variable as used
            } else {
                std::cerr << "Error: variable became null unexpectedly\n";
                return false;
            }

For unknown reason, by doing this, segfaut error disappeared.

### Valgrind

Valgrind was used to check error in memory management. 1st version of forward presented 6 erros while second version presents 1 error on the line that triggered segfault error.
It needs to be patched

### Toy tests

3 Toy tests were created. forward algorithm behave well on them.


## 02/07


### Print functions

Print function that display the execution of the forward algorithm was enhanced : clarity was improved
Print function for pre processing part was created.

### Toy tests

Other toy tests were created : toy tests with and without cycles; deductible and not deductible.
Pre processing as well as forward algorithm were tested on them and behaved really well

### Backward algorithm

The c++ implementation of the backward algorithm was started.
A version that compiles was created. Few details needed to be managed :
- global variables : for memory robustness, it is preferable to pass variables through arguments instead of using global variables (see c++ doc). Then a structure state was created to manage these variables (count, on_line, root)
- functions return type : In Python, AND function return a bool type or rule.successors a list?
  Good care needs to be applied while coding in c++. A solution was proposed but not tested for the moment


## 03/07


### backward algorithm

A second version of the algorithm has been implemented. This time an enumerable VariableState is used
to manage the value of variables (True False None And). In python, value type was a bit strange.
It was bool | None | str.

### Toy test backward

Backward algorithm seems to behave well on the previous toy tests implemented.

### Error in cycle management

Previous toy tests didn't really have a proper cycle. In case of cycles, the algorithm must save Rules and Variables. These are stored in the vector named successors; they must be well managed. AND function didn't handle this case well. It is important to return R.successors vector in order to be processed by OR function. AND function returned only boolean then was not returning vector as it should.

That is why, AND function was declared as std::variant<bool, std::vector<std::weak_ptr<Variable>>>  in  order to be able to return the vector.

Or function was modified accordingly.
This new version behave well on all previous toy tests and on the last toy test that includes a proper cycle.

## 04/07

### documentation

A file : doc_drawer.py was created in order to draw any useful graph for the conception process.
2 graphs were created : benchmark_creation_graph.png and benchmark_load_graph.png. They both show  function calls for the process of benchmark creation and benchmark loading.

### generate_data.cpp

The implementation of generate_data module was started in C++.
generate_benchmark function seems to work well for the first benchmark at least. Further tests should be implemented, still the results for the first benchmark are convicing.

### Structural optimization

Conceiving C++ code for benchmark creation lead to a detection of some non optimized code structures in the python version :
- benchmark modules: benchmark1,2,3,4,5.py files could be summerized in one only file. One int variable num_bench is required to choose between benchmarks
- generate_data.generate_benchmark : Not really clear, can reduce the number of lines
- generate_question : Not well done. It uses a list of str (variable_base []) that would save every variables(str form) of every rules created. Then one str variable of this list is chosen as the question.
It should be much better to hand-construct the question considering the benchmark. 
For example for benchmark 1 with parameters k and n we already know that the question has the form "P.n(k-1)" (n=4,k=6 question="P4.5"). It then costs a lot less than saving every single str variable and choose one.

## 05/07

### classes.cpp

Functions that enable to go from facts_base,rules,question objects in a str form to a class form were implemented (createSet ...). 

### Unicity of object representation

For a specific string, functions from classes.cpp have to create only one object representation of it. For example, if in the set of rules we see multiple rules using proposition "P1", there will be only one Object of class Variable representing P1 in memory. To do so, the code uses an unorderedmap <string,Variable>. During the process of conversion from string ot Variable/Rules we save in the unorderedmap Variables once created. Then, while trying to create a Variable object, we should always check if a Variable representing the same str has already been created before. 

This characteristic of unicity seems important for the data initialization part. Having one representation helps by enabling not to bother about managing doublons.

The functions in create.cpp that have to take care about this unicity aspect are :
create_ant_obj, create_csq_obj, create_fb_obj, create_q_obj.

### shared_ptr and memory managament

In classes.py dictionnay, list of the objects themselves are used. However in cpp, it is sometimes preferable to use vector of shared_ptr of Variable for example. While using shared_ptrs helps in terms of flexibility, it can make the code harder to understand and to use.
For example, create set returns an unorderedmap having input we will give to the algorithms.
This unorderedmap associate str to shared_ptr of any : "rules" , shared_ptr<Rule>
"facts_base", shared_ptr <vector <shared_ptr<Variable>>> "question", shared_ptr<Variable>.

It is necessary to analyze and see if it is the best option or not. 
That is why multiple versions using shared_ptrs in a different way has been created.


## 08/07

### shared and weak pointers

In the first version of classes implementation, only weak pointers were used in order to tackle the cyclic dependency. In fact, a rule object can reference a Variable object with antecedents,conqequent,successors vectors and a Variable object can reference a Rule object with its rules attribute.
This implies a cyclic dependency meaning that if both classes use vectors of shared_pointers only, it is possible that these pointers are never deallocated (see documentation).
In order to solve this issue, it is mandatory to use weak pointer at some point (see documentation).

As this represents the first project in c++, for safety matter, only weak_pointers were used for Rule and Variable class attributes.

However a problem appeared during the execution.
Variables for algorithms execution are created in create_set function, part of generate_data module.
Variables creation are managed using an unordered_map name "variables" in which we store shared_pointers of newly created variables. Throughout create_set, Rules are created. Weak_pointers referencing the Variables are instantiated for creation of antecedents and consequent attributes of Rule class (vector of weak pointer of Variable and weak_ptr of Variable).

The issue comes when create_set is over.
variables unordered map is out of scope, then, it is deallocated. All shared_ptrs on the Variables are deleted. Once deleted, all variables are then deleted because they were the only shared_ptrs referencing them. Without Variables the algorithms cannot be performed.

To patch this, Rule needs to use shared_ptrs on Variables so that Variables are not deleted when shared_ptrs of "variables" unordered_map are deleted.

(Note : look at documentation. If all shared_ptrs referencing the same object are deleted, then this object is deleted)


### New version and execution

A new version using shared_ptrs for Rule class has been implemented. Functions to measure execution time of the algorithms have been implemented.
For benchmark 1, backward algorithm is in fact linear for c++ version.


## 09/07

### Graph drawing

The graph of the execution times for both versions (cpp and python) was drawn. This graph shows both curves with a linear regression. For backward algorithm, benchmark1, k = 5, size_max = 5000, step = 50 repeat = 200, linear behaviour was found for both algorithms with cpp version being approximately 10 times faster than python one. 


### Forward new version

Now that shared_ptrs are used for Rules objects and Variable value is an enumerable type (VariableState), forward algorithm needed to be refactored. Everything works well except for this strange error of segfault caused by the line : auto& variable = facts_base[i].

If variable holds a reference of facts_base[i], segfault is triggered because of the reallocation of facts_bases when enlarged. To tackle this issue, we should make a copy of the shared_pointer using auto variable = facts_base[i]. See 27/06 for more information


## 10/07

### Forward optimization

In the last version of the forward algorithm, vector was used for facts_base. However, considering frequent reallocations, it is much suitable to use a queue instead. A version of the algorithm using queue instead of vector was implemented, not yet tested.

### Meeting with spanish supervisor

The results were presented to the supervisor and a discussion was held about the following of the project.
Questions were asked about the level of tests and documentations that need to be provided.
If consistent, understandable set of tests need to be performed on the algorithm, the supervisor adviced not to take too much time on documentation.
He prefers to work on other points such as SAT solver or the influence of rules order in algorithms execution.


## 11/07

### Forward algorithm with queue

Last version of forward algorithm using a queue instead of a vector has been tested and seems to work well.

## 12/07

### Order of rules

For some benchmarks, the order of the rules can change how the problem is solved. For example, for benchmark 3 representing a complete graph, best complexity is O(1) and worst O(n2) with backward algorithm. 

This is something that must be discussed in the paper so that can be seen in the implementation.

### Benchmarks

Benchmark 5 was implemented and tested in cpp. Benchmark 3 worst case was implemented in cpp.

## 18/07

### Benchmarks

Benchmark 2 was implemented with a different method than previous version. This method is much clearer. The choice of the question for this benchmark has been well implemented. It distinguished based on the parity of n.

## 23/07

### Benchmarks

Benchmark 4 was implemented and behave correctly in regards of both algorithms

## 24/07

### Documentation

Classes diagramm was drawn with an example