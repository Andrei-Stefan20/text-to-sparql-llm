"""
Pipeline utilities for evaluation with error handling, caching, and optimization.
Provides context managers, decorators, and helper functions for reliable execution.
"""

import time
import logging
import functools
from typing import Callable, Any, TypeVar, Optional, Dict, Tuple
from contextlib import contextmanager
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

T = TypeVar('T')

class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class RetryError(PipelineError):
    """Raised when retry limit exceeded."""
    pass

class TimeoutError(PipelineError):
    """Raised when operation times out."""
    pass

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, on_error: Optional[Callable] = None):
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay (exponential backoff)
        on_error: Optional callback on error (receives exception)
    
    Example:
        @retry(max_attempts=3, delay=0.5)
        def fetch_data():
            return api.get()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if on_error:
                        on_error(e)
                    
                    if attempt < max_attempts:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt}/{max_attempts}), "
                            f"retrying in {current_delay:.1f}s: {str(e)[:80]}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise RetryError(
                f"{func.__name__} failed after {max_attempts} attempts: {last_exception}"
            ) from last_exception
        
        return wrapper
    return decorator

def timeout(seconds: float):
    """
    Decorator for timeout enforcement.
    Note: Requires Unix-like system. On Windows, acts as pass-through.
    
    Args:
        seconds: Timeout duration in seconds
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            import signal
            import sys
            
            if sys.platform == 'win32':
                # Timeout mechanism not reliably supported on Windows platform.
                logger.debug(f"Timeout decorator not supported on Windows, skipping for {func.__name__}")
                return func(*args, **kwargs)
            
            def handle_timeout(signum, frame):
                raise TimeoutError(f"{func.__name__} exceeded {seconds}s timeout")
            
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(int(seconds) + 1)  # +1 to allow for small delays
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Cancel alarm
            
            return result
        
        return wrapper
    return decorator

@contextmanager
def timer(operation_name: str):
    """Context manager for performance timing."""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"{operation_name} took {elapsed:.2f}s")

class SimpleCache:
    """Simple file-based cache for retriever embeddings."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path.home() / ".cache" / "sparql-pipeline"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: Dict[str, Any] = {}
    
    def _get_key_hash(self, key: str) -> str:
        """Generate safe cache key from string."""
        import hashlib
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache using memory or file storage.
        
        Tries in-memory cache first, then file-based persistent cache.
        """
        # Try memory cache first for fast access.
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Try file cache as fallback for persistence.
        cache_file = self.cache_dir / f"{self._get_key_hash(key)}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    value = pickle.load(f)
                    self.memory_cache[key] = value
                    return value
            except Exception as e:
                logger.warning(f"Failed to load cache for {key}: {e}")
        
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Store value in both memory and file-based cache."""
        # Store in in-memory cache for quick access.
        self.memory_cache[key] = value
        
        # Store in file cache for persistence across sessions.
        cache_file = self.cache_dir / f"{self._get_key_hash(key)}.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            logger.warning(f"Failed to save cache for {key}: {e}")
    
    def clear(self) -> None:
        """Clear all caches."""
        self.memory_cache.clear()
        import shutil
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

class BatchProcessor:
    """Helper for safe batch processing with progress tracking."""
    
    def __init__(self, items: list, batch_size: int = 10):
        self.items = items
        self.batch_size = batch_size
        self.total = len(items)
        self.processed = 0
        self.failed = 0
    
    def process(self, process_fn: Callable[[Any], None]) -> Tuple[int, int]:
        """
        Process items in batches.
        
        Args:
            process_fn: Function to process each item
            
        Returns:
            Tuple of (processed_count, failed_count)
        """
        for i, item in enumerate(self.items):
            try:
                process_fn(item)
                self.processed += 1
            except Exception as e:
                self.failed += 1
                logger.error(f"Error processing item {i+1}/{self.total}: {e}")
            
            # Log progress updates at regular batch intervals for monitoring.
            if (i + 1) % self.batch_size == 0:
                logger.info(f"Progress: {i+1}/{self.total} (failed: {self.failed})")
        
        return self.processed, self.failed

def validate_sparql_output(raw_output: str) -> Optional[str]:
    """
    Extract and validate SPARQL query from raw LLM output.
    
    Handles various output formats including markdown code blocks,
    plain SPARQL, and text with embedded SPARQL.
    
    Args:
        raw_output: Raw output from LLM generation (may contain formatting).
        
    Returns:
        Cleaned SPARQL query string or None if no valid query found.
    """
    if not raw_output or not isinstance(raw_output, str):
        return None
    
    # First attempt: Extract from markdown code blocks.
    import re
    pattern = r"```(?:sparql)?\s*(SELECT.*?)```"
    match = re.search(pattern, raw_output, re.DOTALL | re.IGNORECASE)
    
    if match:
        query = match.group(1).strip()
    else:
        # Fallback: Extract SELECT statement if no code block found.
        pattern = r"(SELECT\s+.*)"
        match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
        query = match.group(1).strip() if match else raw_output.strip()
    
    # Validate that query starts with SELECT keyword.
    if not query.upper().startswith('SELECT'):
        return None
    
    return query
