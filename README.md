# Rule-Based Systems: Analyzing Forward and Backward Algorithms

This repository focuses on the implementation and analysis of forward and backward algorithms used in propositional rule-based systems. The project includes tools for benchmarking, testing, profiling, and visualizing the performance of these algorithms.

## Table of Contents


- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [Make commands](#make-commands)
  - [JSON and/or Graphs](#json-andor-graphs)
  - [Executing Algorithms on JSON and/or Graphs](#executing-algorithms-on-json-andor-graphs)
  - [Drawing Execution Time Graphs](#drawing-execution-time-graphs)
- [Contributing](#contributing)


## Project Overview

### Problem Statement

In rule-based systems, knowledge is often represented in the form of rules (implications) and facts (known variables). A typical problem involves determining whether a particular conclusion (question) can be inferred from a given set of rules and known facts.

- **Facts Base**: A set of known variables (facts) that are considered to be true.
- **Rules**: Implications that describe how certain facts can imply others (e.g., `A1 ∧ A2 => Q` means that `Q` can be inferred if both `A1` and `A2` are true).
- **Question**: The target variable we want to deduce (e.g., `Q`).

### Algorithms

Two primary approaches are implemented to solve this problem:

1. **Forward Algorithm**: 
   - Starts with the known facts and applies the rules to infer new facts until the question (target variable) is inferred or all possible inferences are made.
   
2. **Backward Algorithm**:
   - Starts with the question and works backward, trying to establish whether the necessary facts can be deduced from the known facts through the application of the rules.

### Goals

- **Performance Analysis**: Compare the execution time and memory usage of the forward and backward algorithms.
- **Benchmarking**: Generate and evaluate different benchmarks to see how the algorithms perform with varying complexity and size.
- **Visualization**: Provide graphical representations of the results to facilitate comparison and understanding.

## Directory Structure

```plaintext
.
├── cpp/                     # C++ implementation files
│   ├── classes.cpp
│   ├── forward.cpp
│   ├── backward.cpp
│   ├── time_measuring.cpp
│   ├── tests.cpp
│   ├── time_preprocessing.cpp
│   ├── size_measuring.cpp
│   └── Makefile             # Makefile for building and running the project
├── python/                  # Python implementation files
│   ├── and_or_graphs.py
│   ├── draw_graphs.py
│   ├── compare/             # Python comparison scripts
├── csv_curves/              # CSV files and generated curves
├── json_andor/              # JSON files for AND-OR graphs
└── README.md                # This README file

```
## Setup and Installation

### Prerequisites

#### C++ Requirements
- **Compiler**: A C++ compiler that supports C++20.
- **Build Tools**: `make` for building the project using the provided Makefile.

#### Python Requirements
- **Python Version**: Python 3.8 or later.
- **Python Packages**: The following Python packages are required:
  - `numpy`: For numerical computations.
  - `pandas`: For data manipulation and analysis.
  - `matplotlib`: For generating graphs and visualizations.
  - `scikit-learn`: For performing regression analysis.
  - `networkx`: For working with graph structures (used in AND-OR graph visualizations).
  
  Additionally, the following Python Standard Library modules are used for time and memory measurement but are not required for processing the cpp algorithms
  - `cProfile`
  - `pstats`
  - `time`
  - `timeit`
  - `perf_counter`

You can install the required Python packages using `pip`:

```bash
pip install numpy pandas matplotlib scikit-learn networkx

```

## Usage

### Overview

The primary implementation of this project is in C++, located in the `cpp/` directory. The project includes several algorithms and tests for forward and backward reasoning in propositional rule-based systems. The provided `Makefile` automates the build and execution process. Below is a detailed guide on how to compile and run the project.

### Make Commands

The `Makefile` includes various targets for compiling and running different parts of the project. Below is an explanation of each command and its purpose.

#### `make all`
- **Description**: This is the default target. It compiles all the main programs in the project, including the time measuring, time preprocessing, and test executables.
- **Usage**: 
  ```bash
  make all

#### `make run_time_measuring num_bench k end step rep algorithm`
- **Description**: Measures the execution times for the specified parameters .
- **Parameters**:
    num_bench: The benchmark number to run.
    k: The value of k used in the benchmark.
    end: The maximum size n for the benchmark.
    step: The step size to increment n.
    rep: The number of repetitions for the execution.
- **Usage**: 
  ```bash
  make run_time_measuring num_bench=<num_bench> k=<k> end=<end> step=<step> rep=<rep> algorithm=<algorithm>
  ```

  #### `make run_time_preprocessing num_bench k end step rep`
- **Description**: Measures the preprocessing phase for the specified parameters .
- **Parameters**:
    num_bench: The benchmark number to run.
    k: The value of k used in the benchmark.
    end: The maximum size n for the benchmark.
    step: The step size to increment n.
    rep: The number of repetitions for the execution.
- **Usage**: 
  ```bash
  make run_time_preprocessing num_bench=<num_bench> k=<k> end=<end> step=<step> rep=<rep>
  ```

  #### `make run_tests`
- **Description**: Runs the tests to check the behaviour of the algorithms .
- **Usage**: 
  ```bash
  make run_tests
  ```
   #### `make run_size_measuring`
- **Description**: Checks the size of the objects .
- **Usage**: 
  ```bash
  make run_size_measuring
  ```

### JSON and/or Graphs

In the `python/and_or_graphs.py` script, you can generate random AND-OR graphs and save them in both JSON and PNG formats in the `json_andor` folder.

#### Command

To generate a random AND-OR graph, use the following command:

```bash
python3 python/and_or_graphs.py <number_of_rules> <max_antecedents_per_rule> <output_filename>
```

### Executing Algorithms on JSON and/or Graphs

The `cpp/tests.cpp` file provides the ability to execute the algorithms on randomly generated AND-OR graphs stored in the `json_andor` folder. By using the `test_json(filename)` function, you can test the forward and backward algorithms on any JSON file generated from the `python/and_or_graphs.py` script.

#### Usage

To execute the algorithms on a JSON file, follow these steps:

1. **Generate a JSON file**: First, generate an AND-OR graph and save it as a JSON file in the `json_andor` folder using the `python/and_or_graphs.py` script.

2. **Run the test on the JSON file**: Use the `test_json(filename)` function in `cpp/tests.cpp` to load and execute the algorithms on the JSON file.

#### Example

```cpp
// Example usage in cpp/tests.cpp
test_json("my_graph.json");
```

### Drawing Execution Time Graphs

The `python/draw_graphs.py` script allows you to visualize the execution times of the forward and backward algorithms by generating graphs based on CSV files. The CSV files, which contain execution time data, are stored in the `csv_curves` folder and are generated by the `time_measuring` executable.

#### Usage

To draw the execution time graphs, use the following command:

```bash
python3 python/draw_graphs.py <csv_forward> <csv_backward>
```

## Contributing

This project was primarily developed by Brice Decurninge, who implemented the majority of the C++ and Python code, including the core algorithms, benchmarking tools, and visualization scripts. The benchmarks, algorithms, `generate_data.py` and `classes.py` within the `python/compare/` directory were based on earlier work by Léa Maïda.

### Acknowledgments

- **Brice Decurninge**: Main contributor and developer of the project, including the C++ implementations and most of the Python scripts.
- **Léa Maïda**: Provided the foundational work in `python/compare/`, upon which the benchmarks and algorithms were based.







