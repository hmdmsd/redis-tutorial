import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import numpy as np
import sqlite3
import os
from utils.redis_client import RedisClient
def run_realistic_workload(use_cache=True):
    """
    Run a realistic workload with a mix of repeated and varied requests
    This simulates real-world access patterns where some items are requested frequently
    """
    # Simulate a mix of traffic with some "hot" movies that are requested multiple times
    hot_movie_ids = ["1", "3", "5"]  # Popular movies requested multiple times 
    other_movie_ids = ["2", "4", "6", "7", "8", "9", "10"]
    
    # Create a workload with repeated requests for popular movies
    workload = []
    for _ in range(3):  # Repeat hot movies 3x
        workload.extend(hot_movie_ids)
    workload.extend(other_movie_ids)  # Add other movies once
    
    # Shuffle to simulate realistic random access
    random.shuffle(workload)
    
    # Clear all caches before the test
    for i in range(1, 11):
        r.client.delete(f"movie_cache:{i}")
        
    # Process the workload
    start_time = time.time()
    hits = 0
    misses = 0
    
    for movie_id in workload:
        _, cache_hit = get_movie_with_cache(movie_id, use_cache)
        if cache_hit:
            hits += 1
        else:
            misses += 1
    
    end_time = time.time()
    
    # Return execution time and hit/miss statistics
    return {
        'execution_time': end_time - start_time,
        'requests': len(workload),
        'cache_hits': hits,
        'cache_misses': misses,
        'hit_ratio': hits / len(workload) if hits > 0 else 0
    }

def compare_cache_performance():
    # Run without cache
    print("Running workload WITHOUT cache...")
    no_cache_results = run_realistic_workload(r,use_cache=False)
    print(f"Execution time: {no_cache_results['execution_time']:.2f} seconds")
    print(f"Requests: {no_cache_results['requests']}")
    print(f"All database queries (no caching)\n")
    
    # Run with cache
    print("Running workload WITH cache...")
    cache_results = run_realistic_workload(r,use_cache=True)
    print(f"Execution time: {cache_results['execution_time']:.2f} seconds")
    print(f"Requests: {cache_results['requests']}")
    print(f"Cache hits: {cache_results['cache_hits']} ({cache_results['hit_ratio']*100:.1f}%)")
    print(f"Cache misses: {cache_results['cache_misses']}")
    
    # Calculate improvement
    improvement = (no_cache_results['execution_time'] - cache_results['execution_time']) / no_cache_results['execution_time'] * 100
    print(f"\nPerformance improvement with caching: {improvement:.1f}%")
    
    # Visualization
    plt.figure(figsize=(12, 5))
    
    # First subplot: Execution time comparison
    plt.subplot(1, 2, 1)
    times = [no_cache_results['execution_time'], cache_results['execution_time']]
    labels = ['Without Cache', 'With Cache']
    plt.bar(labels, times, color=['#ff9999', '#66b3ff'])
    plt.ylabel('Execution Time (seconds)')
    plt.title('Query Execution Time Comparison')
    
    # Add time labels on top of the bars
    for i, time_val in enumerate(times):
        plt.text(i, time_val + 0.1, f"{time_val:.2f}s", ha='center')
    
    # Second subplot: Cache hit/miss pie chart
    plt.subplot(1, 2, 2)
    hits_misses = [cache_results['cache_hits'], cache_results['cache_misses']]
    labels = ['Cache Hits', 'Cache Misses']
    plt.pie(hits_misses, labels=labels, autopct='%1.1f%%', colors=['#99ff99', '#ff9999'])
    plt.title('Cache Hit/Miss Ratio')
    
    plt.tight_layout()
    plt.show()
    
    # Return the results for further analysis
    return no_cache_results, cache_results

# Run a more detailed analysis to show how cache performance improves over time
def analyze_cache_warming():
    # Clear all caches
    for i in range(1, 11):
        r.client.delete(f"movie_cache:{i}")
    
    # Set up workload - 5 iterations of similar access patterns
    iterations = 5
    results = []
    
    print("Analyzing cache warming effect over multiple iterations...")
    
    for i in range(iterations):
        print(f"Iteration {i+1}/{iterations}...")
        result = run_realistic_workload(r,use_cache=True)
        results.append(result)
        
    # Visualization of warming cache
    plt.figure(figsize=(14, 6))
    
    # First plot: Execution time over iterations
    plt.subplot(1, 2, 1)
    execution_times = [r['execution_time'] for r in results]
    plt.plot(range(1, iterations+1), execution_times, marker='o', linestyle='-', linewidth=2)
    plt.xlabel('Iteration')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Cache Performance Improvement Over Time')
    plt.grid(True)
    
    # Second plot: Hit ratio over iterations
    plt.subplot(1, 2, 2)
    hit_ratios = [r['hit_ratio'] * 100 for r in results]
    plt.plot(range(1, iterations+1), hit_ratios, marker='o', linestyle='-', linewidth=2, color='green')
    plt.xlabel('Iteration')
    plt.ylabel('Cache Hit Ratio (%)')
    plt.title('Cache Hit Ratio Improvement Over Time')
    plt.ylim(0, 100)
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Return the results for further analysis
    return results