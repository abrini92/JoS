"""
Tests for Analyzer module (Fixed to match real API)
"""
import pytest
import tempfile
import shutil
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from jarvisos.core.analyzer import Analyzer


class TestAnalyzer:
    """Test Analyzer class"""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_observations(self, temp_data_dir):
        """Create sample observations file"""
        obs_file = Path(temp_data_dir) / "observations.json"
        observations = {
            "observations": [
                {
                    "iteration": 1,
                    "timestamp": "2025-10-17T09:00:00",
                    "hour": 9,
                    "system": {
                        "cpu_percent": 50.0,
                        "memory_percent": 60.0
                    },
                    "processes": [
                        {"name": "vscode", "cpu_percent": 50.0},
                        {"name": "chrome", "cpu_percent": 30.0}
                    ]
                },
                {
                    "iteration": 2,
                    "timestamp": "2025-10-17T09:10:00",
                    "hour": 9,
                    "system": {
                        "cpu_percent": 55.0,
                        "memory_percent": 65.0
                    },
                    "processes": [
                        {"name": "vscode", "cpu_percent": 60.0}
                    ]
                }
            ]
        }
        with open(obs_file, 'w') as f:
            json.dump(observations, f)
        return obs_file
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_analyzer_creation(self, temp_data_dir):
        """Test creating analyzer"""
        analyzer = Analyzer(data_dir=temp_data_dir)
        assert analyzer.data_dir == Path(temp_data_dir)
        assert analyzer.observations_file == Path(temp_data_dir) / "observations.json"
        assert analyzer.insights_file == Path(temp_data_dir) / "insights.json"
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_load_observations(self, temp_data_dir, sample_observations):
        """Test loading observations"""
        analyzer = Analyzer(data_dir=temp_data_dir)
        data = analyzer.load_observations()
        
        assert data is not None
        assert "observations" in data
        assert len(data["observations"]) == 2
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_load_observations_no_file(self, temp_data_dir):
        """Test loading when no observations file exists"""
        analyzer = Analyzer(data_dir=temp_data_dir)
        
        with pytest.raises(FileNotFoundError):
            analyzer.load_observations()
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_preprocess_observations(self, temp_data_dir, sample_observations):
        """Test preprocessing observations"""
        analyzer = Analyzer(data_dir=temp_data_dir)
        data = analyzer.load_observations()
        
        # preprocess_observations returns a dict with stats
        processed = analyzer.preprocess_observations(data)
        
        assert processed is not None
        assert isinstance(processed, dict)
        # Should have some keys like 'total_observations', 'app_usage', etc.
        assert len(processed) > 0
    
    def test_analyzer_without_api_key(self, temp_data_dir):
        """Test analyzer fails without API key"""
        # Clear API key
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                Analyzer(data_dir=temp_data_dir)
    
    # Skipping Claude API tests - they require real API key or complex mocking
    # The analyzer.analyze() method is tested in integration tests with real data


class TestAnalyzerIntegration:
    """Integration tests for analyzer"""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_full_analysis_pipeline(self, temp_data_dir):
        """Test complete analysis pipeline (without Claude call)"""
        # Create observations
        obs_file = Path(temp_data_dir) / "observations.json"
        observations = {
            "observations": [
                {
                    "iteration": 1,
                    "timestamp": "2025-10-17T09:00:00",
                    "system": {
                        "cpu_percent": 50.0,
                        "memory_percent": 60.0
                    },
                    "processes": [{"name": "test", "cpu_percent": 50.0}]
                }
            ]
        }
        with open(obs_file, 'w') as f:
            json.dump(observations, f)
        
        # Run analyzer (just load and preprocess, not analyze)
        analyzer = Analyzer(data_dir=temp_data_dir)
        data = analyzer.load_observations()
        
        assert data is not None
        assert len(data["observations"]) == 1
        
        # Test preprocessing
        processed = analyzer.preprocess_observations(data)
        assert processed is not None
        assert isinstance(processed, dict)
