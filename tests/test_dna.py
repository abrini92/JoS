"""
Tests for User DNA Profiler
"""
import pytest
import tempfile
import shutil
import json
from pathlib import Path
from jarvisos.core.dna import UserDNA


class TestUserDNA:
    """Test UserDNA class"""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_dna_creation(self, temp_data_dir):
        """Test creating DNA profiler"""
        dna = UserDNA(data_dir=temp_data_dir)
        assert dna.profile is not None
        assert "chronotype" in dna.profile
        assert "work_patterns" in dna.profile
    
    def test_save_and_load_profile(self, temp_data_dir):
        """Test saving and loading profile"""
        dna = UserDNA(data_dir=temp_data_dir)
        dna.profile["user_id"] = "test_user"
        dna.profile["name"] = "Test User"
        dna.save_profile()
        
        # Create new instance
        dna2 = UserDNA(data_dir=temp_data_dir)
        assert dna2.profile["user_id"] == "test_user"
        assert dna2.profile["name"] == "Test User"
    
    def test_analyze_observations(self, temp_data_dir):
        """Test analyzing observations"""
        dna = UserDNA(data_dir=temp_data_dir)
        
        # Create sample observations - wrapped in dict with 'observations' key
        observations_data = {
            "observations": [
                {
                    "timestamp": "2025-10-17T09:00:00",
                    "hour": 9,
                    "processes": [
                        {"name": "vscode", "cpu_percent": 50.0},
                        {"name": "chrome", "cpu_percent": 30.0}
                    ],
                    "active_window": "VS Code"
                },
                {
                    "timestamp": "2025-10-17T10:00:00",
                    "hour": 10,
                    "processes": [
                        {"name": "vscode", "cpu_percent": 60.0},
                        {"name": "terminal", "cpu_percent": 20.0}
                    ],
                    "active_window": "Terminal"
                },
                {
                    "timestamp": "2025-10-17T14:00:00",
                    "hour": 14,
                    "processes": [
                        {"name": "chrome", "cpu_percent": 40.0}
                    ],
                    "active_window": "Chrome"
                }
            ]
        }
        
        dna.analyze_observations(observations_data)
        
        # Check that analysis was performed
        assert dna.profile["chronotype"]["peak_hours"] is not None
        assert dna.profile["tool_preferences"] is not None
    
    def test_get_profile_summary(self, temp_data_dir):
        """Test getting profile summary"""
        dna = UserDNA(data_dir=temp_data_dir)
        dna.profile["chronotype"]["type"] = "morning"
        dna.profile["chronotype"]["peak_hours"] = [9, 10]
        
        summary = dna.get_profile_summary()
        # summary is a dict, not a string
        assert isinstance(summary, dict)
        assert "chronotype" in summary
        assert summary["chronotype"] == "morning"
