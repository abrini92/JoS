#!/usr/bin/env python3
"""
JarvisOS - The First Self-Building Operating System
Main CLI Interface
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add jarvisos to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvisos.core.observer import Observer
from jarvisos.core.analyzer import Analyzer
from jarvisos.core.generator import Generator
from jarvisos.core.executor import Executor

console = Console()


def print_banner():
    """Print JarvisOS banner"""
    banner = """
[bold cyan]
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗ ██████╗ ███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝██╔═══██╗██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗██║   ██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║██║   ██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║╚██████╔╝███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
[/bold cyan]
[bold white]The First Self-Building Operating System[/bold white]
[dim]Version 0.1.0 | Open Source | Freedom-First[/dim]
"""
    console.print(banner)


def cmd_observe(args):
    """Observe user behavior"""
    print_banner()
    observer = Observer()
    observer.observe(duration=args.duration, interval=args.interval)


def cmd_analyze(args):
    """Analyze observations with AI"""
    print_banner()
    try:
        analyzer = Analyzer()
        analyzer.analyze()
    except Exception as e:
        console.print(f"\n[bold red]❌ Analysis failed: {e}[/bold red]\n")
        sys.exit(1)


def cmd_generate(args):
    """Generate automation scripts"""
    print_banner()
    try:
        generator = Generator()
        result = generator.generate(task_index=args.task_index)
        
        if result:
            console.print(f"\n[bold green]✨ Next steps:[/bold green]")
            console.print(f"  1. Review the generated script")
            console.print(f"  2. Run: [cyan]jarvis list[/cyan] to see all scripts")
            console.print(f"  3. Run: [cyan]jarvis run 1 --dry-run[/cyan] to preview execution")
            console.print(f"  4. Run: [cyan]jarvis run 1[/cyan] to execute\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Generation failed: {e}[/bold red]\n")
        sys.exit(1)


def cmd_list(args):
    """List available scripts"""
    print_banner()
    executor = Executor()
    executor.display_scripts()


def cmd_run(args):
    """Execute a script"""
    print_banner()
    executor = Executor()
    result = executor.run(
        script_identifier=args.script_id,
        dry_run=args.dry_run,
        timeout=args.timeout
    )
    
    if result['status'] == 'not_found':
        sys.exit(1)


def cmd_summary(args):
    """Show observation summary"""
    print_banner()
    observer = Observer()
    observer.display_summary()


def cmd_status(args):
    """Show system status"""
    print_banner()
    
    # Check for required files
    data_dir = Path("data")
    scripts_dir = Path("generated_scripts")
    
    observations_file = data_dir / "observations.json"
    insights_file = data_dir / "insights.json"
    
    table = Table(title="JarvisOS Status", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details", style="yellow")
    
    # Observer status
    if observations_file.exists():
        import json
        with open(observations_file) as f:
            data = json.load(f)
        obs_count = data.get('metadata', {}).get('total_observations', 0)
        table.add_row("Observer", "✅ Ready", f"{obs_count} observations collected")
    else:
        table.add_row("Observer", "⚠️  No data", "Run 'jarvis observe' to start")
    
    # Analyzer status
    if insights_file.exists():
        import json
        with open(insights_file) as f:
            data = json.load(f)
        analyzed_at = data.get('metadata', {}).get('analyzed_at', 'Unknown')
        table.add_row("Analyzer", "✅ Ready", f"Last analyzed: {analyzed_at[:19]}")
    else:
        table.add_row("Analyzer", "⚠️  No insights", "Run 'jarvis analyze' to analyze")
    
    # Generator status
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py"))
        if scripts:
            table.add_row("Generator", "✅ Ready", f"{len(scripts)} scripts generated")
        else:
            table.add_row("Generator", "⚠️  No scripts", "Run 'jarvis generate' to create")
    else:
        table.add_row("Generator", "⚠️  Not initialized", "Run 'jarvis generate' to start")
    
    # Executor status
    table.add_row("Executor", "✅ Ready", "Ready to execute scripts")
    
    # API Key status
    import os
    if os.getenv("ANTHROPIC_API_KEY"):
        table.add_row("Claude API", "✅ Configured", "API key found")
    else:
        table.add_row("Claude API", "❌ Missing", "Set ANTHROPIC_API_KEY env var")
    
    console.print()
    console.print(table)
    console.print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="JarvisOS - The First Self-Building Operating System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jarvis observe --duration 60 --interval 5    # Observe for 60s
  jarvis analyze                                # Analyze with AI
  jarvis generate                               # Generate automation
  jarvis list                                   # List scripts
  jarvis run 1 --dry-run                       # Preview script
  jarvis run 1                                  # Execute script
  jarvis status                                 # Show status

For more info: https://github.com/yourusername/jarvisos
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Observe command
    observe_parser = subparsers.add_parser('observe', help='Observe user behavior')
    observe_parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Observation duration in seconds (default: 60)'
    )
    observe_parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Observation interval in seconds (default: 5)'
    )
    observe_parser.set_defaults(func=cmd_observe)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze observations with AI')
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate automation scripts')
    generate_parser.add_argument(
        '--task-index',
        type=int,
        default=0,
        help='Task index to generate (0 = first task, default: 0)'
    )
    generate_parser.set_defaults(func=cmd_generate)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available scripts')
    list_parser.set_defaults(func=cmd_list)
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute a script')
    run_parser.add_argument(
        'script_id',
        help='Script ID (number) or name'
    )
    run_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview only, do not execute'
    )
    run_parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Execution timeout in seconds (default: 30)'
    )
    run_parser.set_defaults(func=cmd_run)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    status_parser.set_defaults(func=cmd_status)
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show observation summary')
    summary_parser.set_defaults(func=cmd_summary)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
