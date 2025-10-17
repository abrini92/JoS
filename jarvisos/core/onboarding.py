"""
JarvisOS Onboarding System
First boot interactive experience
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from ..voice.jarvis_voice import JarvisVoice
from ..utils.logger import get_logger

logger = get_logger("jarvisos.onboarding")
console = Console()


class OnboardingManager:
    """Manages first-time user onboarding experience"""
    
    def __init__(self, data_dir: str = "data", use_voice: bool = True):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.onboarding_file = self.data_dir / "onboarding.json"
        self.profile_file = self.data_dir / "user_profile.json"
        
        self.use_voice = use_voice
        self.jarvis = JarvisVoice() if use_voice else None
        
        logger.info("OnboardingManager initialized")
    
    def is_first_boot(self) -> bool:
        """Check if this is the first boot"""
        return not self.onboarding_file.exists()
    
    def mark_onboarding_complete(self):
        """Mark onboarding as completed"""
        data = {
            "completed": True,
            "completed_at": datetime.now().isoformat(),
            "version": "0.2.0"
        }
        
        with open(self.onboarding_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info("Onboarding marked as complete")
    
    def speak_and_print(self, message: str, style: str = ""):
        """Speak and print message"""
        if style:
            console.print(f"[{style}]{message}[/{style}]")
        else:
            console.print(message)
        
        if self.jarvis:
            self.jarvis.speak(message)
    
    def run_onboarding(self) -> Dict:
        """Run complete onboarding flow"""
        console.clear()
        
        # Welcome
        self._welcome()
        
        # Collect user info
        profile = self._collect_user_info()
        
        # Explain system
        self._explain_system()
        
        # Set expectations
        self._set_expectations()
        
        # Final message
        self._goodbye(profile)
        
        # Save profile
        self._save_profile(profile)
        
        # Mark complete
        self.mark_onboarding_complete()
        
        return profile
    
    def _welcome(self):
        """Welcome message"""
        console.print("\n" * 2)
        
        panel = Panel(
            "[bold cyan]JARVISOS[/bold cyan]\n"
            "[dim]The First Self-Building Operating System[/dim]\n\n"
            "[yellow]Welcome to your new intelligent companion.[/yellow]",
            border_style="cyan",
            padding=(1, 4)
        )
        console.print(panel)
        
        console.print("\n")
        
        if self.jarvis:
            self.jarvis.introduce()
        else:
            self.speak_and_print(
                "Hello! I am Jarvis, your personal operating system.",
                "bold green"
            )
        
        console.print("\n")
        self.speak_and_print(
            "I'm going to ask you a few questions to get to know you better.",
            "cyan"
        )
        console.print("\n")
    
    def _collect_user_info(self) -> Dict:
        """Collect user information"""
        profile = {}
        
        # Name
        console.print("[bold]Let's start with the basics.[/bold]\n")
        
        if self.jarvis:
            self.jarvis.speak("What's your name?")
        
        name = Prompt.ask("[cyan]What's your name?[/cyan]")
        profile['name'] = name
        
        self.speak_and_print(
            f"Nice to meet you, {name}!",
            "green"
        )
        console.print()
        
        # Role/Job
        if self.jarvis:
            self.jarvis.speak("What do you do for work?")
        
        role = Prompt.ask(
            "[cyan]What do you do for work?[/cyan]",
            default="Developer"
        )
        profile['role'] = role
        
        self.speak_and_print(
            f"Great! A {role}. I'll optimize for that.",
            "green"
        )
        console.print()
        
        # Work hours
        if self.jarvis:
            self.jarvis.speak("When do you usually start working?")
        
        start_hour = Prompt.ask(
            "[cyan]What time do you usually start working?[/cyan]",
            default="9"
        )
        profile['work_start'] = int(start_hour)
        
        # Goals
        if self.jarvis:
            self.jarvis.speak("What's your main goal with this system?")
        
        goal = Prompt.ask(
            "[cyan]What's your main goal? (productivity/learning/automation/other)[/cyan]",
            default="productivity"
        )
        profile['goal'] = goal
        
        console.print()
        self.speak_and_print(
            "Perfect! I have everything I need.",
            "green"
        )
        
        return profile
    
    def _explain_system(self):
        """Explain how JarvisOS works"""
        console.print("\n")
        console.print("[bold yellow]Here's how I work:[/bold yellow]\n")
        
        explanations = [
            ("🔍 OBSERVE", "I watch how you work - apps you use, patterns, workflows"),
            ("🧠 ANALYZE", "I use AI to understand your behavior and find inefficiencies"),
            ("⚡ GENERATE", "I create custom automation scripts just for you"),
            ("🧬 EVOLVE", "I improve over time using genetic algorithms")
        ]
        
        for title, desc in explanations:
            console.print(f"[cyan]{title}[/cyan]: {desc}")
            if self.jarvis:
                self.jarvis.speak(f"{title}. {desc}")
            console.print()
        
        console.print()
    
    def _set_expectations(self):
        """Set user expectations"""
        console.print("[bold yellow]What to expect:[/bold yellow]\n")
        
        message = (
            "For the next 3 days, I'll observe your workflow silently. "
            "After that, I'll have insights and automation suggestions for you. "
            "The longer you use me, the better I become at helping you."
        )
        
        console.print(f"[dim]{message}[/dim]\n")
        
        if self.jarvis:
            self.jarvis.speak(message)
        
        # Ask for confirmation
        ready = Confirm.ask(
            "[cyan]Ready to start?[/cyan]",
            default=True
        )
        
        if ready:
            self.speak_and_print(
                "Excellent! Let's begin your journey.",
                "bold green"
            )
        else:
            self.speak_and_print(
                "No problem. Take your time. Run 'jarvis onboard' when ready.",
                "yellow"
            )
    
    def _goodbye(self, profile: Dict):
        """Final goodbye message"""
        console.print("\n")
        
        name = profile.get('name', 'there')
        
        message = (
            f"Alright {name}, I'm now active and observing. "
            f"You won't notice me, but I'm learning. "
            f"Check back in 3 days with 'jarvis summary' to see what I've discovered."
        )
        
        panel = Panel(
            f"[bold green]{message}[/bold green]\n\n"
            "[dim]Tip: Use 'jarvis status' anytime to see what I'm doing.[/dim]",
            border_style="green",
            title="[bold]Welcome Aboard![/bold]"
        )
        
        console.print(panel)
        console.print("\n")
        
        if self.jarvis:
            self.jarvis.speak(message)
    
    def _save_profile(self, profile: Dict):
        """Save user profile"""
        profile['created_at'] = datetime.now().isoformat()
        profile['onboarding_version'] = '0.2.0'
        
        with open(self.profile_file, 'w') as f:
            json.dump(profile, f, indent=2)
        
        logger.info(f"User profile saved: {profile['name']}")
    
    def load_profile(self) -> Optional[Dict]:
        """Load user profile"""
        if not self.profile_file.exists():
            return None
        
        with open(self.profile_file) as f:
            return json.load(f)
    
    def get_user_name(self) -> str:
        """Get user name from profile"""
        profile = self.load_profile()
        if profile:
            return profile.get('name', 'there')
        return 'there'


# CLI function
def run_onboarding_cli(use_voice: bool = True):
    """Run onboarding from CLI"""
    manager = OnboardingManager(use_voice=use_voice)
    
    if not manager.is_first_boot():
        console.print("[yellow]⚠️  Onboarding already completed![/yellow]")
        console.print(f"[dim]User: {manager.get_user_name()}[/dim]\n")
        
        redo = Confirm.ask("Do you want to redo onboarding?", default=False)
        if not redo:
            return
    
    profile = manager.run_onboarding()
    
    console.print("\n[bold green]✅ Onboarding complete![/bold green]\n")
    
    return profile


if __name__ == "__main__":
    run_onboarding_cli()
