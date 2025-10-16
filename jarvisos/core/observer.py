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

from ..utils.logger import get_observer_logger

console = Console()
logger = get_observer_logger()


class Observer:
    """Observes user behavior and logs system activity"""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.observations_file = self.output_dir / "observations.json"
        self.observations: List[Dict] = []
        logger.info(f"Observer initialized with output_dir: {output_dir}")

    def get_running_apps(self) -> List[Dict[str, str]]:
        """Get list of currently running applications with resource usage"""
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                # Filter out system processes
                if info['username'] and info['name']:
                    apps.append({
                        'name': info['name'],
                        'pid': info['pid'],
                        'username': info['username'],
                        'cpu_percent': info.get('cpu_percent') or 0,
                        'memory_percent': round(info.get('memory_percent') or 0, 2)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return apps

    def get_system_stats(self) -> Dict:
        """Get current system statistics with extended metrics"""
        vm = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Try to get network connections, fallback if permission denied
        try:
            net_conn = len(psutil.net_connections())
        except (psutil.AccessDenied, PermissionError):
            net_conn = 0
        
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'memory_percent': vm.percent,
            'memory_used_gb': round(vm.used / (1024**3), 2),
            'memory_total_gb': round(vm.total / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_used_gb': round(disk.used / (1024**3), 2),
            'disk_total_gb': round(disk.total / (1024**3), 2),
            'network_connections': net_conn,
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            'timestamp': datetime.now().isoformat()
        }

    def observe(self, duration: int = 60, interval: int = 5) -> None:
        """
        Observe user behavior for a specified duration
        
        Args:
            duration: Total observation time in seconds (default: 60)
            interval: Time between observations in seconds (default: 5)
        """
        logger.info(f"Starting observation: duration={duration}s, interval={interval}s")
        console.print(f"\n[bold cyan]🔍 JarvisOS Observer Starting...[/bold cyan]")
        console.print(f"Duration: {duration}s | Interval: {interval}s\n")

        iterations = duration // interval
        logger.debug(f"Will perform {iterations} observations")
        
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
        
        logger.info(f"Observation complete: {len(self.observations)} observations collected")
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
        
        try:
            with open(self.observations_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved {len(self.observations)} observations to {self.observations_file}")
        except Exception as e:
            logger.error(f"Failed to save observations: {e}", exc_info=True)
            raise

    def load_observations(self) -> Dict:
        """Load observations from JSON file"""
        if not self.observations_file.exists():
            console.print("[yellow]⚠️  No observations file found[/yellow]")
            return {}
        
        with open(self.observations_file, 'r') as f:
            return json.load(f)

    def get_summary(self) -> Dict:
        """Get summary statistics from observations"""
        data = self.load_observations()
        if not data or 'observations' not in data:
            return {}
        
        observations = data['observations']
        
        # Calculate averages
        avg_cpu = sum(obs['system']['cpu_percent'] for obs in observations) / len(observations)
        avg_memory = sum(obs['system']['memory_percent'] for obs in observations) / len(observations)
        
        # Count unique apps
        all_apps = set()
        for obs in observations:
            for app in obs['apps']:
                all_apps.add(app['name'])
        
        # Find top apps by frequency
        app_counts = {}
        for obs in observations:
            for app in obs['apps']:
                app_counts[app['name']] = app_counts.get(app['name'], 0) + 1
        
        top_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_observations': len(observations),
            'unique_apps': len(all_apps),
            'avg_cpu_percent': round(avg_cpu, 2),
            'avg_memory_percent': round(avg_memory, 2),
            'top_apps': top_apps,
            'start_time': data['metadata']['start_time'],
            'end_time': data['metadata']['end_time']
        }

    def display_summary(self) -> None:
        """Display observation summary in console"""
        from rich.table import Table
        
        summary = self.get_summary()
        if not summary:
            console.print("[yellow]⚠️  No observations to summarize[/yellow]")
            return
        
        console.print("\n[bold cyan]📊 Observation Summary[/bold cyan]\n")
        
        # Stats table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Observations", str(summary['total_observations']))
        table.add_row("Unique Apps", str(summary['unique_apps']))
        table.add_row("Avg CPU Usage", f"{summary['avg_cpu_percent']}%")
        table.add_row("Avg Memory Usage", f"{summary['avg_memory_percent']}%")
        table.add_row("Time Range", f"{summary['start_time'][:19]} → {summary['end_time'][:19]}")
        
        console.print(table)
        
        # Top apps
        console.print("\n[bold yellow]🔥 Top 10 Apps:[/bold yellow]")
        for i, (app, count) in enumerate(summary['top_apps'], 1):
            console.print(f"  {i}. {app}: [green]{count}[/green] times")
        
        console.print()


if __name__ == "__main__":
    # Quick test
    observer = Observer()
    observer.observe(duration=30, interval=5)
