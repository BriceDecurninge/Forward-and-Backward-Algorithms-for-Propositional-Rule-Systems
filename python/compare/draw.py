import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

def draw_graph(filename, output_image='execution_time_graph.png'):
    # Read data from CSV
    data = pd.read_csv(filename)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.scatter(data['Size'], data['Time'], color='blue')
    plt.title('Execution Time evolution with Benchmark Size')
    plt.xlabel('Benchmark Size')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


def draw_linear_comparison(python_csv, cpp_csv, output_image='execution_time_comparison.png'):
    # Read data from CSV files
    python_data = pd.read_csv(python_csv)
    cpp_data = pd.read_csv(cpp_csv)
    
    # Extract sizes and execution times
    python_sizes = np.array(python_data['Size']).reshape(-1, 1)
    python_times = np.array(python_data['Time'])
    
    cpp_sizes = np.array(cpp_data['Size']).reshape(-1, 1)
    cpp_times = np.array(cpp_data['Time'])
    
    # Perform linear regression for Python
    python_model = LinearRegression()
    python_model.fit(python_sizes, python_times)
    python_y_pred = python_model.predict(python_sizes)
    
    python_intercept = python_model.intercept_
    python_slope = python_model.coef_[0]
    
    python_r2 = r2_score(python_times, python_y_pred)
    
    # Perform linear regression for C++
    cpp_model = LinearRegression()
    cpp_model.fit(cpp_sizes, cpp_times)
    cpp_y_pred = cpp_model.predict(cpp_sizes)
    
    cpp_intercept = cpp_model.intercept_
    cpp_slope = cpp_model.coef_[0]
    
    cpp_r2 = r2_score(cpp_times, cpp_y_pred)
    
    # Plot data points and regression lines
    plt.figure(figsize=(10, 6))
    
    # Python data points and regression line
    plt.scatter(python_sizes, python_times, color='blue', label='Python Execution Time')
    plt.plot(python_sizes, python_y_pred, color='blue', linestyle='-', label=f'Python Linear Reg.\nIntercept: {python_intercept:.2f}, Slope: {python_slope:.2e}, R^2: {python_r2:.2f}')
    
    # C++ data points and regression line
    plt.scatter(cpp_sizes, cpp_times, color='red', label='C++ Execution Time')
    plt.plot(cpp_sizes, cpp_y_pred, color='red', linestyle='-', label=f'C++ Linear Reg.\nIntercept: {cpp_intercept:.2f}, Slope: {cpp_slope:.2e}, R^2: {cpp_r2:.2f}')
    
    plt.xlabel('Benchmark Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison between Python and C++')
    plt.legend(fontsize='large')
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


def draw_both(bench_name, sizes, exec_timef, exec_timeb, output_image):
    plt.scatter(sizes, exec_timef, color='red', label="forward")
    plt.scatter(sizes, exec_timeb, color='blue', label="backward")

    plt.xlabel('n')
    plt.ylabel('Execution Time')
    plt.title("Execution Times depending on the size of the entry for " + bench_name)
    plt.legend(fontsize='large')
    plt.grid(True)

    plt.savefig(output_image)
    plt.show()


def draw_phases(alg_name, bench_name, sizes, exec_timep, exec_timea, output_image):
    plt.scatter(sizes, exec_timep, color='red', label="preprocessing")
    plt.scatter(sizes, exec_timea, color='blue', label=alg_name + " algorithm")

    plt.xlabel('n')
    plt.ylabel('Execution Time')
    plt.title("Execution Times depending on the size of the entry for " + bench_name)
    plt.legend(fontsize='large')
    plt.grid(True)

    plt.savefig(output_image)
    plt.show()


def draw_linear(alg_name, bench_name, sizes, execution_time, both=False, output_image='linear_regression_graph.png'):
    X = np.array(sizes).reshape(-1, 1)
    y = np.array(execution_time)
    model = LinearRegression()
    model.fit(X, y)
    
    y_pred = model.predict(X)
    
    slope = model.coef_[0]
    intercept = model.intercept_
    r2 = r2_score(y, y_pred)

    slope_scientific = "{:e}".format(slope)
    intercept_scientific = "{:e}".format(intercept)
    
    plt.scatter(X, y, color='blue', label=alg_name)
    plt.plot(X, y_pred, color='red', label=f'Linear Regression Line\nSlope: {slope_scientific}, Intercept: {intercept_scientific}, R^2 Score: {r2:.2f}')
    
    if both:
        plt.xlabel('k and n')
    else:
        plt.xlabel('n')
    
    plt.ylabel('Execution Time')
    plt.title("Execution Times depending on the size of the entry for " + bench_name)
    plt.legend(fontsize='large')
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


def draw_quadratic(alg_name, bench_name, sizes, execution_time, both=False, output_image='quadratic_regression_graph.png'):
    X = np.array(sizes).reshape(-1, 1)
    y = np.array(execution_time)

    poly = PolynomialFeatures(degree=2, interaction_only=False)
    x_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(x_poly, y)

    coefficients = model.coef_
    intercept = model.intercept_
    beta_1 = coefficients[1]
    beta_2 = coefficients[2]

    intercept_sci = "{:.2e}".format(intercept)
    beta_1_sci = "{:.2e}".format(beta_1)
    beta_2_sci = "{:.2e}".format(beta_2)

    y_pred = model.predict(x_poly)
    r2 = r2_score(y, y_pred)

    plt.scatter(X, y, color='blue', label=alg_name)
    
    x_sorted = np.sort(X, axis=0)
    y_pred_sorted = model.predict(poly.transform(x_sorted))

    plt.plot(x_sorted, y_pred_sorted, color='red', label=f'Quadratic Reg.\n($\\beta_0$: {intercept_sci}, $\\beta_1$: {beta_1_sci}, $\\beta_2$: {beta_2_sci}, $R^2$: {r2:.2f})')

    if both:
        plt.xlabel('k and n')
    else:
        plt.xlabel('n')
    
    plt.ylabel('Execution Time')
    plt.title("Execution Times depending on the size of the entry for " + bench_name)
    
    plt.legend(fontsize='large')
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


if __name__ == "__main__":
    filename = "backwardbb1k5n100p10r10.csv"
    draw_graph(filename, output_image="output_graph.png")
