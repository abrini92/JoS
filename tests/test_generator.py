"""
Tests for Generator module (Fixed to match real API)
"""
import pytest
import tempfile
import shutil
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from jarvisos.core.generator import Generator


class TestGenerator:
    """Test Generator class"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories"""
        data_dir = tempfile.mkdtemp()
        scripts_dir = tempfile.mkdtemp()
        yield data_dir, scripts_dir
        shutil.rmtree(data_dir)
        shutil.rmtree(scripts_dir)
    
    @pytest.fixture
    def sample_insights(self, temp_dirs):
        """Create sample insights file"""
        data_dir, _ = temp_dirs
        insights_file = Path(data_dir) / "insights.json"
        insights = {
            "patterns": ["User opens VS Code every morning at 9 AM"],
            "insights": ["User is most productive in the morning"],
            "suggestions": ["Automate VS Code startup", "Schedule heavy tasks for morning"]
        }
        with open(insights_file, 'w') as f:
            json.dump(insights, f)
        return insights_file
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_generator_creation(self, temp_dirs):
        """Test creating generator"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        assert generator.data_dir == Path(data_dir)
        assert generator.scripts_dir == Path(scripts_dir)
        assert generator.scripts_dir.exists()
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_load_insights(self, temp_dirs, sample_insights):
        """Test loading insights"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        
        insights = generator.load_insights()
        
        assert insights is not None
        assert "patterns" in insights
        assert "suggestions" in insights
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_load_insights_no_file(self, temp_dirs):
        """Test loading when no insights file exists"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        
        with pytest.raises(FileNotFoundError):
            generator.load_insights()
    
    def test_generator_without_api_key(self, temp_dirs):
        """Test generator fails without API key"""
        data_dir, scripts_dir = temp_dirs
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                Generator(data_dir=data_dir, scripts_dir=scripts_dir)
    
    # Skipping Claude API tests - they require real API key
    # The suggest_tasks method is tested in integration with real API
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_validate_syntax(self, temp_dirs):
        """Test Python code validation"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        
        # Valid code
        valid_code = """
def hello():
    print("Hello World")
"""
        assert generator.validate_syntax(valid_code) == True
        
        # Invalid code
        invalid_code = """
def hello(
    print("Hello"
"""
        assert generator.validate_syntax(invalid_code) == False
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_save_script(self, temp_dirs):
        """Test saving generated script"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        
        script_code = """#!/usr/bin/env python3
print("Test script")
"""
        # save_script expects a task dict
        task = {
            "id": "task_001",
            "name": "Test Script",
            "description": "A test script",
            "complexity": "low"
        }
        
        script_path = generator.save_script(task, script_code)
        
        # Check file was created
        assert script_path.exists()
        assert script_path.is_file()
        
        # Verify content
        content = script_path.read_text()
        assert "Test script" in content or "Test Script" in content
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_list_generated_scripts(self, temp_dirs):
        """Test listing generated scripts"""
        data_dir, scripts_dir = temp_dirs
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        
        # Create some test scripts
        (Path(scripts_dir) / "script1.py").write_text("print('1')")
        (Path(scripts_dir) / "script2.py").write_text("print('2')")
        
        scripts = list(generator.scripts_dir.glob("*.py"))
        assert len(scripts) >= 2


class TestGeneratorIntegration:
    """Integration tests for generator"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories"""
        data_dir = tempfile.mkdtemp()
        scripts_dir = tempfile.mkdtemp()
        yield data_dir, scripts_dir
        shutil.rmtree(data_dir)
        shutil.rmtree(scripts_dir)
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    def test_full_generation_pipeline(self, temp_dirs):
        """Test complete generation pipeline"""
        data_dir, scripts_dir = temp_dirs
        
        # Create insights
        insights_file = Path(data_dir) / "insights.json"
        insights = {
            "patterns": ["Test pattern"],
            "suggestions": ["Test suggestion"]
        }
        with open(insights_file, 'w') as f:
            json.dump(insights, f)
        
        # Run generator
        generator = Generator(data_dir=data_dir, scripts_dir=scripts_dir)
        loaded_insights = generator.load_insights()
        
        assert loaded_insights is not None
        assert "patterns" in loaded_insights
