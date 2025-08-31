"""
Custom exceptions for the keyword extraction framework
"""

from typing import Optional, Dict, Any


class KeywordExtractionError(Exception):
    """Base exception for keyword extraction errors"""
    
    def __init__(self, message: str, method: Optional[str] = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.method = method
        self.details = details or {}
    
    def __str__(self):
        base_msg = super().__str__()
        if self.method:
            base_msg = f"[{self.method}] {base_msg}"
        return base_msg


class ModelNotFoundError(KeywordExtractionError):
    """Raised when required models are not available"""
    pass


class InvalidTextError(KeywordExtractionError):
    """Raised when input text is invalid"""
    pass


class ExtractionTimeoutError(KeywordExtractionError):
    """Raised when extraction times out"""
    pass


class ConfigurationError(KeywordExtractionError):
    """Raised when there are configuration issues"""
    pass


class DependencyError(KeywordExtractionError):
    """Raised when required dependencies are missing"""
    pass


class BenchmarkError(KeywordExtractionError):
    """Raised when benchmarking fails"""
    pass


class ValidationError(KeywordExtractionError):
    """Raised when validation fails"""
    pass


# Exception handling utilities

def handle_extraction_error(func):
    """Decorator to handle common extraction errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImportError as e:
            raise DependencyError(f"Missing dependency: {e}", details={'original_error': str(e)})
        except FileNotFoundError as e:
            raise ModelNotFoundError(f"Model file not found: {e}", details={'original_error': str(e)})
        except ValueError as e:
            raise InvalidTextError(f"Invalid input: {e}", details={'original_error': str(e)})
        except Exception as e:
            # Re-raise as generic KeywordExtractionError if not already our custom exception
            if isinstance(e, KeywordExtractionError):
                raise
            raise KeywordExtractionError(f"Unexpected error: {e}", details={'original_error': str(e)})
    return wrapper


async def handle_extraction_error_async(func):
    """Async decorator to handle common extraction errors"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ImportError as e:
            raise DependencyError(f"Missing dependency: {e}", details={'original_error': str(e)})
        except FileNotFoundError as e:
            raise ModelNotFoundError(f"Model file not found: {e}", details={'original_error': str(e)})
        except ValueError as e:
            raise InvalidTextError(f"Invalid input: {e}", details={'original_error': str(e)})
        except Exception as e:
            # Re-raise as generic KeywordExtractionError if not already our custom exception
            if isinstance(e, KeywordExtractionError):
                raise
            raise KeywordExtractionError(f"Unexpected error: {e}", details={'original_error': str(e)})
    return wrapper