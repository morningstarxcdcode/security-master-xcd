# Benchmarking script for core functionalities
import time
from aibuddy import core

def benchmark_function():
    start_time = time.time()
    core.some_function()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    benchmark_function()