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
from jarvisos.core.evolution import GenePool, EvolutionEngine
from jarvisos.core.dna import UserDNA
from jarvisos.core.onboarding import OnboardingManager
from jarvisos.core.notifier import ProactiveNotifier
from jarvisos.core.context import ContextAnalyzer, SmartInterruptionManager
from jarvisos.core.feedback import FeedbackManager, FeedbackIntegration
from jarvisos.voice.jarvis_voice import JarvisVoice
from jarvisos.core.self_improver import SelfImprover

# Predictive Engine V2 - TOP 0.1%
try:
    from jarvisos.core.ai_brain import AIBrain
    from jarvisos.core.operational_intelligence import OperationalIntelligence
    from jarvisos.core.tactical_intelligence import TacticalIntelligence
    PREDICTIVE_ENGINE_AVAILABLE = True
except ImportError:
    PREDICTIVE_ENGINE_AVAILABLE = False

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


def cmd_dna(args):
    """Show user DNA profile"""
    print_banner()
    dna = UserDNA()
    
    # Load and analyze observations if available
    obs_file = Path("data/observations.json")
    if obs_file.exists():
        import json
        with open(obs_file) as f:
            observations_data = json.load(f)
        dna.analyze_observations(observations_data)
    
    dna.display_profile()


def cmd_evolve(args):
    """Run evolution cycle"""
    print_banner()
    console.print("\n[bold cyan]🧬 Running Evolution Cycle...[/bold cyan]\n")
    
    gene_pool = GenePool()
    engine = EvolutionEngine(gene_pool)
    
    result = engine.evolve()
    
    # Display results
    console.print("[bold green]✅ Evolution Complete![/bold green]\n")
    console.print(f"[yellow]Mutations created:[/yellow] {result['mutations_created']}")
    console.print(f"[yellow]Genes selected:[/yellow] {result['genes_selected']}")
    console.print(f"[yellow]Average fitness:[/yellow] {result['evaluation']['avg_fitness']}\n")
    
    # Show top genes
    if result['evaluation']['top_genes']:
        console.print("[bold]🏆 Top Performing Genes:[/bold]")
        for gene in result['evaluation']['top_genes']:
            console.print(f"  • {gene['name']}: [green]{gene['fitness']}[/green]")
        console.print()


def cmd_genes(args):
    """List all genes in gene pool"""
    print_banner()
    gene_pool = GenePool()
    
    active_genes = gene_pool.get_active_genes()
    
    if not active_genes:
        console.print("\n[yellow]No genes in pool yet. Generate some scripts first![/yellow]\n")
        return
    
    table = Table(title="🧬 Gene Pool", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Fitness", style="green")
    table.add_column("Executions", style="yellow")
    table.add_column("Status", style="blue")
    
    for gene in sorted(active_genes, key=lambda g: g.fitness_score, reverse=True):
        table.add_row(
            gene.id[:8],
            gene.name,
            f"{gene.fitness_score:.3f}",
            str(gene.execution_count),
            gene.status
        )
    
    console.print()
    console.print(table)
    console.print()


def cmd_speak(args):
    """Test Jarvis voice"""
    print_banner()
    
    jarvis = JarvisVoice()
    
    if args.text:
        # Speak provided text
        jarvis.speak(args.text)
    elif args.greet:
        # Greet user
        jarvis.greet()
    elif args.introduce:
        # Full introduction
        jarvis.introduce()
    else:
        # Default test
        jarvis.speak("Hello. I am Jarvis. Your personal operating system.")


def cmd_listen(args):
    """Test speech recognition"""
    print_banner()
    
    jarvis = JarvisVoice()
    
    console.print("\n[yellow]🎤 Listening... (speak now)[/yellow]\n")
    
    text = jarvis.listen(timeout=args.timeout)
    
    if text:
        console.print(f"\n[green]✅ You said:[/green] {text}\n")
        
        if args.respond:
            jarvis.speak(f"You said: {text}")
    else:
        console.print("\n[red]❌ No speech detected[/red]\n")


def cmd_onboard(args):
    """Interactive onboarding - New immersive experience"""
    from jarvisos.onboarding import JarvisOnboarding
    
    onboarding = JarvisOnboarding()
    onboarding.run()


def cmd_notify(args):
    """Check and send notifications"""
    notifier = ProactiveNotifier()
    notifier.check_and_notify()


def cmd_greet(args):
    """Morning greeting"""
    manager = OnboardingManager()
    user_name = manager.get_user_name()
    
    notifier = ProactiveNotifier()
    notifier.morning_greeting(user_name)


def cmd_context(args):
    """Show current context"""
    print_banner()
    
    analyzer = ContextAnalyzer()
    
    # Load observations
    obs_file = Path("data/observations.json")
    if not obs_file.exists():
        console.print("[red]❌ No observations found. Run 'jarvis observe' first.[/red]\n")
        return
    
    import json
    with open(obs_file) as f:
        data = json.load(f)
    
    observations = data.get('observations', [])
    
    if not observations:
        console.print("[red]❌ No observations to analyze.[/red]\n")
        return
    
    # Current context
    latest = observations[-1]
    context = analyzer.detect_context(latest)
    
    console.print(f"\n[bold cyan]🧠 Current Context:[/bold cyan] [yellow]{context}[/yellow]\n")
    
    # Session analysis
    recent = observations[-12:] if len(observations) >= 12 else observations
    session = analyzer.analyze_session(recent)
    
    console.print("[bold]📊 Recent Session:[/bold]")
    console.print(f"  Dominant: {session['dominant_context']}")
    console.print(f"  Focus Time: {session['focus_time']} min")
    console.print(f"  Productive: {'✅ Yes' if session['productive'] else '❌ No'}")
    
    # Can interrupt?
    can_interrupt = analyzer.should_interrupt()
    console.print(f"\n[bold]🔔 Can Interrupt:[/bold] {'✅ Yes' if can_interrupt else '❌ No (in focus/meeting)'}\n")


def cmd_rate(args):
    """Rate a script"""
    print_banner()
    
    manager = FeedbackManager()
    
    if args.script_id:
        # Rate specific script
        manager.prompt_for_feedback(args.script_id, args.script_id)
    else:
        # Show feedback summary
        manager.display_feedback_summary()


def cmd_feedback(args):
    """Show feedback summary"""
    print_banner()
    
    manager = FeedbackManager()
    manager.display_feedback_summary()


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


def cmd_predict(args):
    """Predict what user needs next - AI-powered"""
    if not PREDICTIVE_ENGINE_AVAILABLE:
        console.print("[red]Predictive Engine not available[/red]")
        return
    
    data_dir = Path("data")
    
    console.print("\n[bold cyan]🔮 AI-Powered Prediction[/bold cyan]\n")
    
    # Initialize
    ai_brain = AIBrain(data_dir)
    op_intel = OperationalIntelligence(data_dir, ai_brain)
    
    # Get current action
    action = args.action if args.action else "Current activity"
    
    console.print(f"[dim]Analyzing: {action}[/dim]\n")
    
    # Process action
    result = op_intel.process_user_action(action)
    
    # Show predictions
    predictions = result['predictions']
    
    if predictions:
        table = Table(title="🔮 Predictions", show_header=True)
        table.add_column("Action", style="cyan")
        table.add_column("Confidence", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Reason", style="dim")
        
        for pred in predictions[:5]:
            table.add_row(
                pred['action'][:40],
                f"{pred['confidence']:.0%}",
                pred['priority'].upper(),
                pred['reason'][:60] + "..."
            )
        
        console.print(table)
    else:
        console.print("[yellow]No predictions at this time[/yellow]")
    
    console.print()


def cmd_plan(args):
    """Plan a work session - Strategic AI"""
    if not PREDICTIVE_ENGINE_AVAILABLE:
        console.print("[red]Predictive Engine not available[/red]")
        return
    
    data_dir = Path("data")
    goal = " ".join(args.goal)
    
    console.print("\n[bold cyan]🎯 Strategic Session Planning[/bold cyan]\n")
    console.print(f"[bold]Goal:[/bold] {goal}\n")
    
    # Initialize
    ai_brain = AIBrain(data_dir)
    tactical = TacticalIntelligence(ai_brain)
    
    console.print("[dim]AI is creating your strategic plan...[/dim]\n")
    
    # Create plan
    plan = tactical.plan_work_session(goal)
    
    # Display plan
    console.print(Panel(
        f"[bold]Duration:[/bold] {plan.estimated_duration_minutes} minutes\n"
        f"[bold]Optimal Start:[/bold] {plan.optimal_start_time}\n"
        f"[bold]Phases:[/bold] {len(plan.phases)}",
        title="📋 Session Plan",
        border_style="cyan"
    ))
    
    console.print()
    
    # Show phases
    for i, phase in enumerate(plan.phases, 1):
        console.print(f"[bold cyan]Phase {i}:[/bold cyan] {phase.name} [dim]({phase.duration_minutes} min)[/dim]")
        for action in phase.actions[:3]:
            console.print(f"  • {action}")
        if phase.break_after:
            console.print("  [yellow]→ Break recommended after this phase[/yellow]")
        console.print()
    
    # Show success criteria
    if plan.success_criteria:
        console.print("[bold green]Success Criteria:[/bold green]")
        for criterion in plan.success_criteria:
            console.print(f"  ✓ {criterion}")
        console.print()


def cmd_suggest(args):
    """Get proactive suggestions"""
    if not PREDICTIVE_ENGINE_AVAILABLE:
        console.print("[red]Predictive Engine not available[/red]")
        return
    
    print_banner()
    
    # Get operational intelligence
    op_intel = OperationalIntelligence()
    suggestions = op_intel.get_proactive_suggestions()
    
    if not suggestions:
        console.print("\n[cyan]✨ Everything looks good! No urgent suggestions.[/cyan]\n")
        return
    
    console.print("\n[bold cyan]💡 Proactive Suggestions[/bold cyan]\n")
    
    for i, suggestion in enumerate(suggestions, 1):
        priority_color = {
            'critical': 'red',
            'high': 'yellow',
            'medium': 'cyan',
            'low': 'green'
        }.get(suggestion.priority, 'white')
        
        console.print(f"[{priority_color}]{i}. [{suggestion.priority.upper()}] {suggestion.type}[/{priority_color}]")
        console.print(f"   {suggestion.message}")
        
        if suggestion.action:
            console.print(f"   💡 Action: [cyan]{suggestion.action}[/cyan]")
        console.print()


def cmd_improvements(args):
    """Show self-improvement suggestions"""
    print_banner()
    
    improver = SelfImprover()
    improvements = improver.get_improvements(status=args.status if hasattr(args, 'status') else None)
    
    if not improvements:
        console.print("\n[cyan]✨ No improvements yet! Keep using JarvisOS.[/cyan]\n")
        console.print("[dim]The self-improvement engine monitors your patterns and suggests optimizations.[/dim]\n")
        return
    
    console.print(f"\n[bold cyan]🧬 Self-Improvements ({len(improvements)})[/bold cyan]\n")
    
    for imp in improvements:
        status_emoji = {
            'pending': '⏳',
            'approved': '✅',
            'rejected': '❌'
        }.get(imp['status'], '❓')
        
        risk_color = {
            'low': 'green',
            'moderate': 'yellow',
            'high': 'red'
        }.get(imp['risk_level'], 'white')
        
        console.print(f"{status_emoji} [bold]ID {imp['id']}[/bold] - [{risk_color}]{imp['risk_level'].upper()} RISK[/{risk_color}]")
        console.print(f"   Pattern: {imp['pattern']['command']} ({imp['pattern']['count']}x)")
        console.print(f"   Type: {imp['pattern']['type']}")
        console.print(f"   Suggestion: {imp['suggestion']}")
        console.print()


def cmd_approve(args):
    """Approve an improvement"""
    print_banner()
    
    improver = SelfImprover()
    improvements = improver.get_improvements(status='pending')
    
    # Find improvement by ID
    improvement = None
    for imp in improvements:
        if imp['id'] == args.improvement_id:
            improvement = imp
            break
    
    if not improvement:
        console.print(f"\n[red]❌ Improvement ID {args.improvement_id} not found[/red]\n")
        return
    
    console.print(f"\n[bold]Approving improvement {improvement['id']}...[/bold]")
    console.print(f"Pattern: {improvement['pattern']['command']}")
    console.print(f"Risk: {improvement['risk_level']}")
    console.print()
    
    # TODO: Apply improvement
    console.print("[green]✅ Approved! (Implementation in v1.0)[/green]\n")


def cmd_self_status(args):
    """Show self-improvement status"""
    print_banner()
    
    improver = SelfImprover()
    
    pending = improver.get_improvements(status='pending')
    approved = improver.get_improvements(status='approved')
    
    console.print("\n[bold cyan]🧬 Self-Improvement Status[/bold cyan]\n")
    console.print(f"Pending improvements: {len(pending)}")
    console.print(f"Approved improvements: {len(approved)}")
    console.print()
    
    if pending:
        console.print("[yellow]💡 Run 'jarvis improvements' to review pending suggestions[/yellow]\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='JarvisOS - The First Self-Building Operating System',
        formatter_class=argparse.RawDescriptionHelpFormatter
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
    
    # DNA command
    dna_parser = subparsers.add_parser('dna', help='Show user DNA profile')
    dna_parser.set_defaults(func=cmd_dna)
    
    # Evolve command
    evolve_parser = subparsers.add_parser('evolve', help='Run evolution cycle')
    evolve_parser.set_defaults(func=cmd_evolve)
    
    # Genes command
    genes_parser = subparsers.add_parser('genes', help='List all genes in pool')
    genes_parser.set_defaults(func=cmd_genes)
    
    # Speak command
    speak_parser = subparsers.add_parser('speak', help='Test Jarvis voice')
    speak_parser.add_argument('--text', type=str, help='Text to speak')
    speak_parser.add_argument('--greet', action='store_true', help='Greet user')
    speak_parser.add_argument('--introduce', action='store_true', help='Full introduction')
    speak_parser.set_defaults(func=cmd_speak)
    
    # Listen command
    listen_parser = subparsers.add_parser('listen', help='Test speech recognition')
    listen_parser.add_argument('--timeout', type=int, default=10, help='Listening timeout')
    listen_parser.add_argument('--respond', action='store_true', help='Speak back what was heard')
    listen_parser.set_defaults(func=cmd_listen)
    
    # Onboard command
    onboard_parser = subparsers.add_parser('onboard', help='Interactive onboarding')
    onboard_parser.add_argument('--no-voice', action='store_true', help='Disable voice')
    onboard_parser.set_defaults(func=cmd_onboard)
    
    # Notify command (for system use)
    notify_parser = subparsers.add_parser('notify', help='Check and send notifications')
    notify_parser.set_defaults(func=cmd_notify)
    
    # Greet command
    greet_parser = subparsers.add_parser('greet', help='Morning greeting')
    greet_parser.set_defaults(func=cmd_greet)
    
    # Context command
    context_parser = subparsers.add_parser('context', help='Show current context')
    context_parser.set_defaults(func=cmd_context)
    
    # Rate command
    rate_parser = subparsers.add_parser('rate', help='Rate a script')
    rate_parser.add_argument('script_id', nargs='?', help='Script ID to rate')
    rate_parser.set_defaults(func=cmd_rate)
    
    # Feedback command
    feedback_parser = subparsers.add_parser('feedback', help='Show feedback summary')
    feedback_parser.set_defaults(func=cmd_feedback)
    
    # Predictive Engine commands (V2 - TOP 0.1%)
    if PREDICTIVE_ENGINE_AVAILABLE:
        # Predict command
        predict_parser = subparsers.add_parser('predict', help='🔮 Predict what you need next (AI-powered)')
        predict_parser.add_argument('--action', type=str, help='Current action')
        predict_parser.set_defaults(func=cmd_predict)
        
        # Plan command
        plan_parser = subparsers.add_parser('plan', help='🎯 Plan a work session (Strategic AI)')
        plan_parser.add_argument('goal', nargs='+', help='Your goal')
        plan_parser.set_defaults(func=cmd_plan)
        
        # Suggest command
        suggest_parser = subparsers.add_parser('suggest', help='💡 Get proactive suggestions')
        suggest_parser.set_defaults(func=cmd_suggest)
    
    # Self-Improvement commands
    improvements_parser = subparsers.add_parser('improvements', help='🧬 View self-improvement suggestions')
    improvements_parser.add_argument('--status', choices=['pending', 'approved', 'rejected'], help='Filter by status')
    improvements_parser.set_defaults(func=cmd_improvements)
    
    approve_parser = subparsers.add_parser('approve', help='✅ Approve an improvement')
    approve_parser.add_argument('improvement_id', help='Improvement ID to approve')
    approve_parser.set_defaults(func=cmd_approve)
    
    self_status_parser = subparsers.add_parser('self-status', help='🔍 Self-improvement engine status')
    self_status_parser.set_defaults(func=cmd_self_status)
    
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
