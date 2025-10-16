"""
Analyzer - Uses Claude AI to analyze user behavior patterns
"""

import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

console = Console()


class Analyzer:
    """Analyzes user behavior using Claude AI"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.observations_file = self.data_dir / "observations.json"
        self.insights_file = self.data_dir / "insights.json"
        
        # Initialize Claude API
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found in environment variables.\n"
                "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
            )
        
        self.client = Anthropic(api_key=api_key)

    def load_observations(self) -> Dict:
        """Load observations from JSON file"""
        if not self.observations_file.exists():
            raise FileNotFoundError(
                f"❌ Observations file not found: {self.observations_file}\n"
                "Run 'jarvis observe' first to collect data."
            )
        
        with open(self.observations_file, 'r') as f:
            return json.load(f)

    def preprocess_observations(self, data: Dict) -> Dict:
        """Preprocess observations for analysis"""
        observations = data.get('observations', [])
        
        # Count app usage
        app_counter = Counter()
        for obs in observations:
            for app in obs.get('apps', []):
                app_counter[app['name']] += 1
        
        # Extract timestamps
        timestamps = [obs['timestamp'] for obs in observations]
        
        # Calculate average system stats
        cpu_avg = sum(obs['system']['cpu_percent'] for obs in observations) / len(observations)
        mem_avg = sum(obs['system']['memory_percent'] for obs in observations) / len(observations)
        
        return {
            'total_observations': len(observations),
            'most_used_apps': app_counter.most_common(10),
            'timestamps': timestamps,
            'avg_cpu': round(cpu_avg, 2),
            'avg_memory': round(mem_avg, 2),
            'unique_apps': len(app_counter)
        }

    def analyze_with_claude(self, preprocessed_data: Dict) -> Dict:
        """Send data to Claude for AI analysis"""
        console.print("\n[bold cyan]🤖 Analyzing with Claude AI...[/bold cyan]\n")
        
        # Prepare prompt for Claude
        prompt = f"""You are analyzing user behavior data from JarvisOS, a self-building operating system.

Here's the data collected:

**Observation Summary:**
- Total observations: {preprocessed_data['total_observations']}
- Unique applications: {preprocessed_data['unique_apps']}
- Average CPU usage: {preprocessed_data['avg_cpu']}%
- Average Memory usage: {preprocessed_data['avg_memory']}%

**Most Used Applications:**
{chr(10).join(f"- {app[0]}: {app[1]} times" for app in preprocessed_data['most_used_apps'])}

**Time Range:**
- Start: {preprocessed_data['timestamps'][0]}
- End: {preprocessed_data['timestamps'][-1]}

Please analyze this data and provide:

1. **Usage Patterns**: What patterns do you see in the user's behavior?
2. **Time Patterns**: Any time-of-day patterns?
3. **Automation Opportunities**: What tasks could be automated? (List 3-5 specific suggestions)
4. **System Health**: Any concerns about CPU/memory usage?
5. **Recommendations**: What should JarvisOS focus on building for this user?

Respond in JSON format with these exact keys:
{{
  "usage_patterns": ["pattern1", "pattern2", ...],
  "time_patterns": ["pattern1", "pattern2", ...],
  "automation_opportunities": [
    {{"task": "task name", "description": "why automate this", "priority": "high/medium/low"}},
    ...
  ],
  "system_health": {{"status": "good/warning/critical", "notes": "..."}},
  "recommendations": ["rec1", "rec2", ...]
}}
"""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse JSON response
            insights = json.loads(response_text)
            
            # Add metadata
            insights['metadata'] = {
                'analyzed_at': datetime.now().isoformat(),
                'model': 'claude-3-haiku-20240307',
                'observations_count': preprocessed_data['total_observations']
            }
            
            return insights
            
        except Exception as e:
            console.print(f"[bold red]❌ Error calling Claude API: {e}[/bold red]")
            raise

    def save_insights(self, insights: Dict) -> None:
        """Save insights to JSON file"""
        with open(self.insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
        
        console.print(f"[bold green]💾 Insights saved to: {self.insights_file}[/bold green]\n")

    def display_insights(self, insights: Dict) -> None:
        """Display insights in a beautiful format"""
        console.print("\n" + "="*70)
        console.print(Panel.fit(
            "[bold cyan]🧠 JarvisOS AI Insights[/bold cyan]",
            border_style="cyan"
        ))
        
        # Usage Patterns
        console.print("\n[bold yellow]📊 Usage Patterns:[/bold yellow]")
        for pattern in insights.get('usage_patterns', []):
            console.print(f"  • {pattern}")
        
        # Time Patterns
        console.print("\n[bold yellow]⏰ Time Patterns:[/bold yellow]")
        for pattern in insights.get('time_patterns', []):
            console.print(f"  • {pattern}")
        
        # Automation Opportunities
        console.print("\n[bold yellow]🤖 Automation Opportunities:[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Priority", style="yellow")
        
        for opp in insights.get('automation_opportunities', []):
            table.add_row(
                opp.get('task', ''),
                opp.get('description', ''),
                opp.get('priority', '').upper()
            )
        
        console.print(table)
        
        # System Health
        health = insights.get('system_health', {})
        status = health.get('status', 'unknown')
        status_color = {
            'good': 'green',
            'warning': 'yellow',
            'critical': 'red'
        }.get(status, 'white')
        
        console.print(f"\n[bold yellow]💚 System Health:[/bold yellow]")
        console.print(f"  Status: [bold {status_color}]{status.upper()}[/bold {status_color}]")
        console.print(f"  Notes: {health.get('notes', 'N/A')}")
        
        # Recommendations
        console.print("\n[bold yellow]💡 Recommendations:[/bold yellow]")
        for rec in insights.get('recommendations', []):
            console.print(f"  • {rec}")
        
        console.print("\n" + "="*70 + "\n")

    def analyze(self) -> Dict:
        """Main analysis workflow"""
        console.print("\n[bold cyan]🔬 Starting Analysis...[/bold cyan]")
        
        # Load observations
        console.print("📂 Loading observations...")
        data = self.load_observations()
        
        # Preprocess
        console.print("⚙️  Preprocessing data...")
        preprocessed = self.preprocess_observations(data)
        
        # Analyze with Claude
        insights = self.analyze_with_claude(preprocessed)
        
        # Save insights
        self.save_insights(insights)
        
        # Display insights
        self.display_insights(insights)
        
        return insights


if __name__ == "__main__":
    # Quick test
    analyzer = Analyzer()
    analyzer.analyze()
