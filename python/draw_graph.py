"""
Execution Time Analysis and Visualization Script

This Python script provides tools for analyzing and visualizing the execution times of algorithms
(such as forward and backward algorithms) across different benchmark sizes. The script can read 
execution time data from CSV files, perform quadratic or exponential regression to model the 
execution time trends, and generate visualizations of these trends. The visualizations can be 
saved as PNG images for further analysis or presentation.


Usage:
------
To run the script, use the following command in your terminal:

    python draw.py <csv_forward_file> <csv_backward_file>

Where:
- `<csv_forward_file>`: The CSV file containing execution times for the forward algorithm.
- `<csv_backward_file>`: The CSV file containing execution times for the backward algorithm.


"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import sys
import os



def exponential_func(x, a, b, c):
    """Exponential function for curve fitting."""
    return a * np.exp(b * x) + c

def draw_regression(ax, alg_name, sizes, execution_times, color, regression_type='quadratic'):
    """
    Draws the regression line (quadratic or exponential) for the given data.

    Args:
        ax: The matplotlib axis object to draw on.
        alg_name: Name of the algorithm for labeling.
        sizes: The sizes of benchmarks.
        execution_times: The execution times corresponding to the sizes.
        color: The color of the plot.
        regression_type: Type of regression ('quadratic' or 'exponential').
    """
    X = np.array(sizes).reshape(-1, 1)
    y = np.array(execution_times)
    
    if regression_type == 'quadratic':
        poly = PolynomialFeatures(degree=2, interaction_only=False)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        y_pred = model.predict(X_poly)
        coefficients = model.coef_
        intercept = model.intercept_
        r2 = r2_score(y, y_pred)
        
        # Plot regression curve
        ax.plot(np.sort(X, axis=0), np.sort(y_pred), color=color, linestyle='--', label=f'{alg_name} quadratic regression ($R^2$: {r2:.2f})')
        
    elif regression_type == 'exponential':
        popt, _ = curve_fit(exponential_func, X.flatten(), y, maxfev=10000)
        y_pred = exponential_func(X.flatten(), *popt)
        residuals = y - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r2 = 1 - (ss_res / ss_tot)
        
        # Plot regression curve
        ax.plot(np.sort(X.flatten()), np.sort(y_pred), color=color, linestyle='--', label=f'{alg_name} exponential regression ($R^2$: {r2:.2f})')
    
    # Plot original data points
    ax.scatter(X, y, color=color, label=f'{alg_name} data')


def draw_reg(forward_filename, backward_filename, regression_type='quadratic'):
    """
    Draws a comparison of execution times with quadratic or exponential regression for forward and backward algorithms.

    Args:
        forward_filename: CSV file containing forward algorithm execution times.
        backward_filename: CSV file containing backward algorithm execution times.
        regression_type: Type of regression ('quadratic' or 'exponential').
    """

    
    output_folder = "../csv_curves/"
    os.makedirs(output_folder, exist_ok=True)


    forward_filename = os.path.join(output_folder, forward_filename)
    backward_filename = os.path.join(output_folder, backward_filename)

    # Extracting num_bench and k from the filename
    filename_components = os.path.basename(forward_filename).split('b')
    num_bench = filename_components[1].split('k')[0]
    k = filename_components[1].split('k')[1].split('n')[0]

    forward_data = pd.read_csv(forward_filename)
    backward_data = pd.read_csv(backward_filename)

    fig, ax = plt.subplots(figsize=(12, 8))
    
    draw_regression(ax, 'Forward Algorithm', forward_data['Size'], forward_data['Time'], 'blue', regression_type)
    draw_regression(ax, 'Backward Algorithm', backward_data['Size'], backward_data['Time'], 'red', regression_type)
    
    ax.set_title(f'Execution Time Evolution with Benchmark {num_bench} k={k}')
    ax.set_xlabel('Size')
    ax.set_ylabel('Execution Time (seconds)')
    ax.legend()
    ax.grid(True)
    
    
    output_filename = os.path.basename(forward_filename).replace('forward','').replace('.csv', '.png')
    output_path = os.path.join(output_folder, output_filename)
    
    plt.savefig(output_path)
    plt.show()

def draw_graph(filename):
    """
    Draws a simple scatter plot of execution time vs benchmark size.

    Args:
        filename: CSV file containing execution times.
    """
    data = pd.read_csv(filename)

    plt.figure(figsize=(10, 6))
    plt.scatter(data['Size'], data['Time'], color='blue')
    plt.title('Execution Time evolution with Benchmark Size')
    plt.xlabel('Benchmark Size')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.savefig('execution_time_graph.png')
    plt.show()

def draw_graphs(forward_filename, backward_filename):
    """
    Draws a comparison scatter plot of execution times for forward and backward algorithms.

    Args:
        forward_filename: CSV file containing forward algorithm execution times.
        backward_filename: CSV file containing backward algorithm execution times.
    """
    forward_data = pd.read_csv(forward_filename)
    backward_data = pd.read_csv(backward_filename)

    plt.figure(figsize=(10, 6))
    
    plt.scatter(forward_data['Size'], forward_data['Time'], color='blue', label='Forward Algorithm')
    plt.scatter(backward_data['Size'], backward_data['Time'], color='red', label='Backward Algorithm')
    
    plt.title('Execution Time Evolution with Benchmark Size')
    plt.xlabel('Benchmark Size')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('execution_time_comparison_graph.png')
    plt.show()

def main():
    if len(sys.argv) != 3:
        print("Usage: python draw.py <csv_forward_file> <csv_backward_file> ")
        sys.exit(1)

    forward_filename = sys.argv[1]
    backward_filename = sys.argv[2]
    

    regression_type = 'quadratic'  # or 'exponential'

    draw_reg(forward_filename, backward_filename,regression_type)
    
    # draw_reg(forward_filename, backward_filename, regression_type='exponential')

if __name__ == "__main__":
    main()
