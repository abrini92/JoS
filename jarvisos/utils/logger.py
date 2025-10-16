"""
JarvisOS Logging System
Centralized logging for all modules
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

console = Console()


class JarvisLogger:
    """Centralized logger for JarvisOS"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str, log_file: Optional[str] = None) -> logging.Logger:
        """
        Get or create a logger
        
        Args:
            name: Logger name (usually module name)
            log_file: Optional log file path
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Create logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # File handler - detailed logs
        if log_file is None:
            log_file = logs_dir / f"jarvisos_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            log_file = logs_dir / log_file
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler - Rich output
        console_handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True
        )
        console_handler.setLevel(logging.INFO)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Cache logger
        cls._loggers[name] = logger
        
        return logger


def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional custom log file
        
    Returns:
        Configured logger
        
    Example:
        >>> from jarvisos.utils import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Starting observation")
        >>> logger.error("Failed to connect", exc_info=True)
    """
    return JarvisLogger.get_logger(name, log_file)


# Pre-configured loggers for common modules
def get_observer_logger():
    """Get logger for Observer module"""
    return get_logger("jarvisos.observer", "observer.log")


def get_analyzer_logger():
    """Get logger for Analyzer module"""
    return get_logger("jarvisos.analyzer", "analyzer.log")


def get_generator_logger():
    """Get logger for Generator module"""
    return get_logger("jarvisos.generator", "generator.log")


def get_executor_logger():
    """Get logger for Executor module"""
    return get_logger("jarvisos.executor", "executor.log")


if __name__ == "__main__":
    # Test logging
    logger = get_logger("test")
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    try:
        1 / 0
    except Exception:
        logger.exception("Exception with traceback")
    
    console.print("\n[green]✅ Logging test complete![/green]")
    console.print(f"Check logs/ directory for log files")
