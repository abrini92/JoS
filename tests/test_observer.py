"""
Tests for Observer module
"""

import json
import pytest
from pathlib import Path
from jarvisos.core.observer import Observer


class TestObserver:
    """Test Observer functionality"""
    
    @pytest.fixture
    def observer(self, tmp_path):
        """Create observer with temporary directory"""
        return Observer(output_dir=str(tmp_path))
    
    def test_observer_init(self, observer, tmp_path):
        """Test observer initialization"""
        assert observer.output_dir == tmp_path
        assert observer.observations_file == tmp_path / "observations.json"
        assert observer.observations == []
    
    def test_get_running_apps(self, observer):
        """Test getting running apps"""
        apps = observer.get_running_apps()
        assert isinstance(apps, list)
        assert len(apps) > 0
        
        # Check app structure
        app = apps[0]
        assert 'name' in app
        assert 'pid' in app
        assert 'username' in app
        assert 'cpu_percent' in app
        assert 'memory_percent' in app
    
    def test_get_system_stats(self, observer):
        """Test getting system stats"""
        stats = observer.get_system_stats()
        assert isinstance(stats, dict)
        
        # Check required fields
        required_fields = [
            'cpu_percent', 'cpu_count',
            'memory_percent', 'memory_used_gb', 'memory_total_gb',
            'disk_percent', 'disk_used_gb', 'disk_total_gb',
            'network_connections', 'boot_time', 'timestamp'
        ]
        
        for field in required_fields:
            assert field in stats
    
    def test_observe_short_duration(self, observer):
        """Test short observation"""
        observer.observe(duration=4, interval=2)
        
        assert len(observer.observations) == 2
        assert observer.observations_file.exists()
    
    def test_save_and_load_observations(self, observer):
        """Test saving and loading observations"""
        # Create mock observations
        observer.observations = [
            {
                'iteration': 1,
                'timestamp': '2025-10-17T00:00:00',
                'apps': [{'name': 'test', 'pid': 1, 'username': 'user', 'cpu_percent': 0, 'memory_percent': 0}],
                'system': {'cpu_percent': 10, 'memory_percent': 50, 'disk_percent': 30, 'timestamp': '2025-10-17T00:00:00'}
            }
        ]
        
        # Save
        observer.save_observations()
        assert observer.observations_file.exists()
        
        # Load
        data = observer.load_observations()
        assert 'metadata' in data
        assert 'observations' in data
        assert data['metadata']['total_observations'] == 1
    
    def test_get_summary(self, observer):
        """Test getting summary"""
        # Create and save mock observations
        observer.observations = [
            {
                'iteration': 1,
                'timestamp': '2025-10-17T00:00:00',
                'apps': [
                    {'name': 'app1', 'pid': 1, 'username': 'user', 'cpu_percent': 0, 'memory_percent': 0},
                    {'name': 'app2', 'pid': 2, 'username': 'user', 'cpu_percent': 0, 'memory_percent': 0}
                ],
                'system': {'cpu_percent': 20, 'memory_percent': 60, 'disk_percent': 30, 'timestamp': '2025-10-17T00:00:00'}
            },
            {
                'iteration': 2,
                'timestamp': '2025-10-17T00:00:05',
                'apps': [
                    {'name': 'app1', 'pid': 1, 'username': 'user', 'cpu_percent': 0, 'memory_percent': 0}
                ],
                'system': {'cpu_percent': 30, 'memory_percent': 70, 'disk_percent': 30, 'timestamp': '2025-10-17T00:00:05'}
            }
        ]
        observer.save_observations()
        
        # Get summary
        summary = observer.get_summary()
        
        assert summary['total_observations'] == 2
        assert summary['unique_apps'] == 2
        assert summary['avg_cpu_percent'] == 25.0
        assert summary['avg_memory_percent'] == 65.0
        assert len(summary['top_apps']) == 2
        assert summary['top_apps'][0][0] == 'app1'  # Most frequent
        assert summary['top_apps'][0][1] == 2  # Appeared 2 times
