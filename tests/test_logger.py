"""
Tests for Logger utility
"""

import pytest
import logging
from pathlib import Path
from jarvisos.utils.logger import get_logger, JarvisLogger


class TestLogger:
    """Test logging functionality"""
    
    def test_get_logger(self):
        """Test getting a logger"""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"
    
    def test_logger_caching(self):
        """Test that loggers are cached"""
        logger1 = get_logger("test_cache")
        logger2 = get_logger("test_cache")
        assert logger1 is logger2
    
    def test_logger_levels(self):
        """Test logger has correct levels"""
        logger = get_logger("test_levels")
        assert logger.level == logging.DEBUG
    
    def test_log_file_creation(self):
        """Test that log files are created"""
        logger = get_logger("test_file", "test_custom.log")
        logger.info("Test message")
        
        log_file = Path("logs/test_custom.log")
        assert log_file.exists()
    
    def test_specialized_loggers(self):
        """Test specialized logger functions"""
        from jarvisos.utils.logger import (
            get_observer_logger,
            get_analyzer_logger,
            get_generator_logger,
            get_executor_logger
        )
        
        obs_logger = get_observer_logger()
        assert obs_logger.name == "jarvisos.observer"
        
        ana_logger = get_analyzer_logger()
        assert ana_logger.name == "jarvisos.analyzer"
        
        gen_logger = get_generator_logger()
        assert gen_logger.name == "jarvisos.generator"
        
        exe_logger = get_executor_logger()
        assert exe_logger.name == "jarvisos.executor"
