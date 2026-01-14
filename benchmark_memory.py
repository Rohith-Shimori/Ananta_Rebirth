import time
import os
import sqlite3
import shutil
# Mocking DATA_DIR creation to avoid errors if it doesn't exist yet
import memory.adaptive_memory
memory.adaptive_memory.DATA_DIR = "."

from memory.adaptive_memory import AdaptiveMemory

# Use a temporary DB file for benchmarking
BENCHMARK_DB = "benchmark_memory.db"

class BenchmarkAdaptiveMemory(AdaptiveMemory):
    def __init__(self):
        # Override db_path to avoid touching the real database
        self.db_path = BENCHMARK_DB
        # Initialize connection as parent does now
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_database()

def benchmark():
    if os.path.exists(BENCHMARK_DB):
        os.remove(BENCHMARK_DB)

    print(f"Benchmarking with DB: {BENCHMARK_DB}")
    mem = BenchmarkAdaptiveMemory()

    start_time = time.time()

    # Perform a sequence of operations
    iterations = 100
    print(f"Running {iterations} iterations...")
    for i in range(iterations):
        mem.add_memory("user", f"Test memory {i}", importance=5)
        if i % 10 == 0:
            mem.get_recent_memories(limit=5)
        if i % 50 == 0:
             mem.get_statistics()

    # Close connection before ending benchmark to be clean
    mem.close()

    end_time = time.time()
    duration = end_time - start_time

    print(f"Total time for {iterations} iterations: {duration:.4f} seconds")
    print(f"Average time per iteration: {duration/iterations*1000:.4f} ms")

    # Cleanup
    if os.path.exists(BENCHMARK_DB):
        os.remove(BENCHMARK_DB)

if __name__ == "__main__":
    benchmark()
