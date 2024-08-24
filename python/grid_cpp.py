"""
Grid'5000 Execution and Data Retrieval Script

This Python script is designed to automate the process of retrieving benchmark execution data 
from the Grid'5000 infrastructure, storing it locally, and then generating visualizations 
using the retrieved data. The script supports both forward and backward algorithms, with 
options for preprocessing the data.

Usage:
------
To run the script, use the following command in your terminal:

    python grid_cpp.py <num_bench> <k> <max> <step> <rep> <site_id>

Where:
- `<num_bench>`: The number of of the benchmark to process.
- `<k>`: A size related parameter.
- `<max>`: The maximum size of the benchmark.
- `<step>`: The step size used in the benchmark.
- `<rep>`: The number of repetitions for the executions.
- `<site_id>`: The Grid'5000 site ID from which to retrieve the data.

Pay attention to the local and remote path
"""

import os
import sys

def main():

    if len(sys.argv) != 7:
        print("Usage: python grid_cpp.py <num_bench> <k> <max> <step> <rep> <site_id>")
        sys.exit(1)

    
    num_bench = int(sys.argv[1])
    k = int(sys.argv[2])
    size_max = int(sys.argv[3])
    step = int(sys.argv[4])
    repetitions = int(sys.argv[5])
    site_id = sys.argv[6]


    user = input(f"Grid'5000 username (default is {os.getlogin()}): ") or os.getlogin()
    pre_processing = False

    # Location of the saved data :
    local_path = "../csv_curves/"
    os.makedirs(local_path, exist_ok=True)

    f_file_name = "forwardb" + str(num_bench) + 'k' + str(k) + 'n' + str(size_max) + 'p' + str(step) + 'r' + str(repetitions)+ ".csv"
    b_file_name = "backwardb" + str(num_bench) + 'k' + str(k) + 'n' + str(size_max) + 'p' + str(step) + 'r' + str(repetitions)+ ".csv"
    
    if (pre_processing):
        f_file_name = "pre_" + f_file_name
        b_file_name = "pre_" + b_file_name

    f_remote_file_path = "csv_curves/"+f_file_name
    b_remote_file_path = "csv_curves/"+b_file_name


    f_local_file_name = site_id +"_"+ f_file_name
    f_local_file_path = os.path.join(local_path, f_local_file_name )

    b_local_file_name = site_id +"_"+ b_file_name
    b_local_file_path = os.path.join(local_path, b_local_file_name )


    # scp commands :
    f_scp_command = f"scp {user}@access.grid5000.fr:{site_id}/{f_remote_file_path} {f_local_file_path}"
    b_scp_command = f"scp {user}@access.grid5000.fr:{site_id}/{b_remote_file_path} {b_local_file_path}"
    os.system(f_scp_command)
    print(f"Result copied to {f_local_file_path}")
    os.system(b_scp_command)
    print(f"Result copied to {b_local_file_path}")

    # drawing command
    draw_command = f"python3 draw_graph.py {f_local_file_path} {b_local_file_path} "
    os.system(draw_command)
    

if __name__ == "__main__":
    main()
