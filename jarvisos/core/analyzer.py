"""
Analyzer - Uses AI (Ollama or Claude) to analyze user behavior patterns
"""

import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

try:
    from .ai_brain_unified import get_unified_brain
except ImportError:
    from jarvisos.core.ai_brain_unified import get_unified_brain

console = Console()


class Analyzer:
    """Analyzes user behavior using AI (Ollama-first, Claude fallback)"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.observations_file = self.data_dir / "observations.json"
        self.insights_file = self.data_dir / "insights.json"
        
        # Initialize unified AI brain (Ollama-first)
        self.ai = get_unified_brain()

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

    def analyze_with_ai(self, preprocessed_data: Dict) -> Dict:
        """Send data to AI for analysis (Ollama-first, Claude fallback)"""
        console.print("\n[bold cyan]🤖 Analyzing with AI...[/bold cyan]\n")
        
        # Prepare prompt
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
            # Use unified AI brain (Ollama or Claude)
            console.print(f"[dim]Using: {self.ai.__class__.__name__}[/dim]")
            console.print(f"[dim]AI Status: {self.ai.get_status_message()}[/dim]")
            
            response_text = self.ai.generate(prompt)
            
            # Check if AI returned something
            if not response_text:
                console.print("[red]⚠️  AI returned None. Checking availability...[/red]")
                console.print(f"[dim]Active backend: {self.ai.active}[/dim]")
                if self.ai.ollama_brain:
                    console.print(f"[dim]Ollama available: {self.ai.ollama_brain.available}[/dim]")
                raise ValueError("AI returned no response. Check if Ollama is running and model is installed.")
            
            # Parse JSON response
            # Try to extract JSON if response contains extra text
            if '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                response_text = response_text[json_start:json_end]
            
            insights = json.loads(response_text)
            
            # Add metadata
            insights['metadata'] = {
                'analyzed_at': datetime.now().isoformat(),
                'ai_backend': self.ai.__class__.__name__,
                'observations_count': preprocessed_data['total_observations']
            }
            
            return insights
            
        except json.JSONDecodeError as e:
            console.print(f"[bold yellow]⚠️  AI response wasn't valid JSON. Attempting to parse...[/bold yellow]")
            # Fallback: create basic insights from response
            insights = {
                'usage_patterns': ['AI analysis in progress'],
                'time_patterns': ['Pattern detection'],
                'automation_opportunities': [
                    {'task': 'Analysis', 'description': 'AI is learning your patterns', 'priority': 'medium'}
                ],
                'system_health': {'status': 'good', 'notes': 'System running normally'},
                'recommendations': ['Continue using JarvisOS to improve AI learning'],
                'metadata': {
                    'analyzed_at': datetime.now().isoformat(),
                    'ai_backend': self.ai.__class__.__name__,
                    'observations_count': preprocessed_data['total_observations'],
                    'note': 'Fallback response due to JSON parsing error'
                }
            }
            return insights
            
        except Exception as e:
            console.print(f"[bold red]❌ Error calling AI: {e}[/bold red]")
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
        
        # Analyze with AI (Ollama-first)
        insights = self.analyze_with_ai(preprocessed)
        
        # Save insights
        self.save_insights(insights)
        
        # Display insights
        self.display_insights(insights)
        
        return insights


if __name__ == "__main__":
    # Quick test
    analyzer = Analyzer()
    analyzer.analyze()
