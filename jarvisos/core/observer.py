"""
Observer - Monitors user behavior and system activity
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class Observer:
    """Observes user behavior and logs system activity"""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.observations_file = self.output_dir / "observations.json"
        self.observations: List[Dict] = []

    def get_running_apps(self) -> List[Dict[str, str]]:
        """Get list of currently running applications"""
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                info = proc.info
                # Filter out system processes
                if info['username'] and info['name']:
                    apps.append({
                        'name': info['name'],
                        'pid': info['pid'],
                        'username': info['username']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return apps

    def get_system_stats(self) -> Dict:
        """Get current system statistics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }

    def observe(self, duration: int = 60, interval: int = 5) -> None:
        """
        Observe user behavior for a specified duration
        
        Args:
            duration: Total observation time in seconds (default: 60)
            interval: Time between observations in seconds (default: 5)
        """
        console.print(f"\n[bold cyan]🔍 JarvisOS Observer Starting...[/bold cyan]")
        console.print(f"Duration: {duration}s | Interval: {interval}s\n")

        iterations = duration // interval
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Observing...", total=iterations)
            
            for i in range(iterations):
                # Collect observation data
                observation = {
                    'iteration': i + 1,
                    'timestamp': datetime.now().isoformat(),
                    'apps': self.get_running_apps(),
                    'system': self.get_system_stats()
                }
                
                self.observations.append(observation)
                
                progress.update(task, advance=1)
                
                if i < iterations - 1:  # Don't sleep on last iteration
                    time.sleep(interval)

        # Save observations
        self.save_observations()
        
        console.print(f"\n[bold green]✅ Observation complete![/bold green]")
        console.print(f"📊 Collected {len(self.observations)} observations")
        console.print(f"💾 Saved to: {self.observations_file}\n")

    def save_observations(self) -> None:
        """Save observations to JSON file"""
        data = {
            'metadata': {
                'total_observations': len(self.observations),
                'start_time': self.observations[0]['timestamp'] if self.observations else None,
                'end_time': self.observations[-1]['timestamp'] if self.observations else None,
            },
            'observations': self.observations
        }
        
        with open(self.observations_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_observations(self) -> Dict:
        """Load observations from JSON file"""
        if not self.observations_file.exists():
            console.print("[yellow]⚠️  No observations file found[/yellow]")
            return {}
        
        with open(self.observations_file, 'r') as f:
            return json.load(f)


if __name__ == "__main__":
    # Quick test
    observer = Observer()
    observer.observe(duration=30, interval=5)
