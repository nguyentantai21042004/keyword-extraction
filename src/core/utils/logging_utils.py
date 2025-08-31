"""
Logging utilities for the keyword extraction framework
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

from ...config.config_manager import get_config, LogLevel


class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(logger_name: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration"""
    config = get_config()
    log_config = config.logging
    
    # Get or create logger
    logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Set level
    log_level = getattr(logging, log_config.level.value)
    logger.setLevel(log_level)
    
    # Console handler
    if log_config.console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Use colored formatter for console
        console_formatter = ColoredFormatter(log_config.format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_config.file_enabled:
        log_file_path = Path(log_config.file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use rotating file handler to prevent huge log files
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        
        # Use standard formatter for file
        file_formatter = logging.Formatter(log_config.format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return setup_logging(name)


class LoggerMixin:
    """Mixin class to add logging capabilities"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        if not hasattr(self, '_logger'):
            class_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
            self._logger = get_logger(class_name)
        return self._logger


# Context managers for logging
class LogContext:
    """Context manager for logging operations"""
    
    def __init__(self, logger: logging.Logger, operation: str, level: int = logging.INFO):
        self.logger = logger
        self.operation = operation
        self.level = level
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.perf_counter()
        self.logger.log(self.level, f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.perf_counter() - self.start_time
        
        if exc_type is None:
            self.logger.log(self.level, f"Completed {self.operation} in {duration:.3f}s")
        else:
            self.logger.error(f"Failed {self.operation} after {duration:.3f}s: {exc_val}")
        
        return False  # Don't suppress exceptions