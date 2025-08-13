"""
Performance measurement utilities
"""

import time
import psutil
from typing import Callable, Any
from functools import wraps

def measure_performance(func: Callable) -> Callable:
    """Decorator to measure function performance"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Add performance metrics to result if it has attributes
            if hasattr(result, 'processing_time'):
                result.processing_time = end_time - start_time
            if hasattr(result, 'memory_usage'):
                result.memory_usage = end_memory - start_memory
            
            return result
            
        except Exception as e:
            # Return error result with performance metrics
            if hasattr(args[0], 'method_name'):
                method_name = args[0].method_name
            else:
                method_name = 'unknown'
            
            # Create a simple result object
            class ErrorResult:
                def __init__(self):
                    self.processing_time = time.time() - start_time
                    self.memory_usage = 0
                    self.method_name = method_name
                    self.error = str(e)
            
            return ErrorResult()
    
    return wrapper
