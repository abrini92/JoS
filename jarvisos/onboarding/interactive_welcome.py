#!/usr/bin/env python3
"""
JarvisOS - Interactive Welcome & Onboarding
The first experience when booting JarvisOS
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Optional

try:
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    import speech_recognition as sr
    LISTEN_AVAILABLE = True
except ImportError:
    LISTEN_AVAILABLE = False

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.text import Text


console = Console()


class JarvisOnboarding:
    """Interactive onboarding experience"""
    
    def __init__(self):
        self.user_name = None
        self.user_role = None
        self.voice_enabled = VOICE_AVAILABLE
        self.listen_enabled = LISTEN_AVAILABLE
        self.config_path = Path.home() / ".jarvisos" / "profile.json"
        
        # Initialize voice
        if self.voice_enabled:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)  # Speed
            self.engine.setProperty('volume', 0.9)
    
    def speak(self, text: str):
        """Jarvis speaks"""
        if self.voice_enabled:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass  # Fallback silently
    
    def listen(self) -> Optional[str]:
        """Jarvis listens (optional)"""
        if not self.listen_enabled:
            return None
        
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                console.print("[cyan]🎤 Listening...[/cyan]")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                return text
        except:
            return None
    
    def display_logo(self):
        """Display JarvisOS logo"""
        logo = """
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗ ██████╗ ███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝██╔═══██╗██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗██║   ██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║██║   ██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║╚██████╔╝███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
        """
        
        console.clear()
        console.print(Align.center(Text(logo, style="bold cyan")))
        console.print(Align.center("[bold white]The Self-Building Operating System[/bold white]"))
        console.print()
        time.sleep(1)
    
    def boot_sequence(self):
        """Simulate boot sequence"""
        console.clear()
        
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[cyan]{task.description}"),
            console=console
        ) as progress:
            
            tasks = [
                "Initializing Arc Reactor Core",
                "Loading AI Brain (Claude Haiku)",
                "Activating Predictive Engine",
                "Starting Operational Intelligence",
                "Enabling Tactical Intelligence",
                "Booting JarvisOS"
            ]
            
            for task_name in tasks:
                task = progress.add_task(task_name, total=1)
                time.sleep(0.5)
                progress.update(task, advance=1)
        
        console.print("\n[bold green]✅ JarvisOS Online[/bold green]\n")
        time.sleep(1)
    
    def welcome_message(self):
        """Jarvis introduces himself"""
        console.clear()
        self.display_logo()
        
        welcome = Panel(
            "[cyan]Hello. I am Jarvis.\n\n"
            "I'm not just an operating system.\n"
            "I'm your intelligent assistant that learns from you,\n"
            "predicts what you need, and automates your work.\n\n"
            "Let me get to know you.[/cyan]",
            title="[bold cyan]🤖 Welcome[/bold cyan]",
            border_style="cyan"
        )
        
        console.print(welcome)
        self.speak("Hello. I am Jarvis. Welcome to JarvisOS. Let me get to know you.")
        time.sleep(2)
    
    def ask_name(self):
        """Ask user's name"""
        console.print()
        
        # Try voice first (optional)
        if self.listen_enabled:
            self.speak("What is your name?")
            console.print("[cyan]💬 Jarvis:[/cyan] What is your name?")
            console.print("[dim](You can type or speak)[/dim]\n")
            
            name = self.listen()
            if name:
                console.print(f"[green]🎤 Heard: {name}[/green]")
                confirm = Confirm.ask(f"Did I hear correctly: {name}?")
                if confirm:
                    self.user_name = name
                    return
        
        # Fallback to typing
        self.speak("What is your name?")
        console.print("[cyan]💬 Jarvis:[/cyan] What is your name?")
        self.user_name = Prompt.ask("[bold]Your name[/bold]")
    
    def greet_user(self):
        """Personalized greeting"""
        console.print()
        greeting = f"Nice to meet you, {self.user_name}! 👋"
        console.print(f"[cyan]💬 Jarvis:[/cyan] {greeting}")
        self.speak(f"Nice to meet you, {self.user_name}")
        time.sleep(1)
    
    def ask_role(self):
        """Ask what user does"""
        console.print()
        self.speak("What do you do? Are you a developer, designer, or something else?")
        console.print("[cyan]💬 Jarvis:[/cyan] What do you do?")
        
        roles = [
            "Developer",
            "Designer",
            "Data Scientist",
            "DevOps/SRE",
            "Student",
            "Other"
        ]
        
        console.print("\n[bold]Choose your role:[/bold]")
        for i, role in enumerate(roles, 1):
            console.print(f"  {i}. {role}")
        
        choice = Prompt.ask("\nYour choice", choices=[str(i) for i in range(1, len(roles)+1)])
        self.user_role = roles[int(choice)-1]
        
        if self.user_role == "Other":
            self.user_role = Prompt.ask("Tell me more")
    
    def show_features(self):
        """Quick feature tour"""
        console.print()
        self.speak("Let me show you what I can do for you.")
        console.print("[cyan]💬 Jarvis:[/cyan] Let me show you what I can do:\n")
        
        features = [
            ("🔮 Predict", "I predict what you need before you ask"),
            ("🎯 Plan", "I help you plan your work sessions strategically"),
            ("🤖 Automate", "I generate scripts from your behavior"),
            ("📊 Observe", "I learn from everything you do"),
            ("💡 Suggest", "I give you proactive suggestions"),
        ]
        
        for icon, desc in features:
            console.print(f"  [bold cyan]{icon}[/bold cyan] [white]{desc}[/white]")
            time.sleep(0.8)
        
        console.print()
        time.sleep(1)
    
    def quick_demo(self):
        """Quick demo"""
        console.print()
        self.speak("Want to see a quick demo?")
        
        if Confirm.ask("[cyan]💬 Jarvis:[/cyan] Want to see a quick demo?", default=True):
            console.print("\n[bold cyan]🎬 Quick Demo[/bold cyan]\n")
            
            with Progress(SpinnerColumn(style="cyan"), TextColumn("[cyan]{task.description}")) as progress:
                progress.add_task("Analyzing your system...", total=None)
                time.sleep(2)
            
            console.print("[green]✅ Analysis complete![/green]\n")
            console.print("[cyan]💬 Jarvis:[/cyan] I noticed you're on a fresh system.")
            console.print("[cyan]💬 Jarvis:[/cyan] Would you like me to set up your dev environment?\n")
            
            self.speak("I noticed you're on a fresh system. I can help you set it up.")
    
    def save_profile(self):
        """Save user profile"""
        profile = {
            "name": self.user_name,
            "role": self.user_role,
            "onboarding_completed": True,
            "first_boot": time.time()
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(profile, f, indent=2)
    
    def final_message(self):
        """Final message"""
        console.print()
        
        message = Panel(
            f"[cyan]Perfect, {self.user_name}!\n\n"
            f"I'm ready to help you with your {self.user_role.lower()} work.\n\n"
            f"I'll be learning from you and getting smarter every day.\n\n"
            f"Let's build something amazing together! 🚀[/cyan]",
            title="[bold cyan]🤖 Ready![/bold cyan]",
            border_style="cyan"
        )
        
        console.print(message)
        self.speak(f"Perfect, {self.user_name}! I'm ready to help. Let's build something amazing together!")
        time.sleep(2)
        
        console.print("\n[bold]Quick commands:[/bold]")
        console.print("  [cyan]jarvis status[/cyan]    - Check system status")
        console.print("  [cyan]jarvis predict[/cyan]   - Get AI predictions")
        console.print("  [cyan]jarvis plan[/cyan]      - Plan your work session")
        console.print("  [cyan]jarvis --help[/cyan]    - See all commands\n")
    
    def run(self):
        """Run full onboarding"""
        try:
            # Check if already onboarded
            if self.config_path.exists():
                with open(self.config_path) as f:
                    profile = json.load(f)
                    if profile.get('onboarding_completed'):
                        console.print("[dim]Onboarding already completed. Use --force to run again.[/dim]")
                        return
            
            # Full onboarding flow
            self.boot_sequence()
            self.welcome_message()
            self.ask_name()
            self.greet_user()
            self.ask_role()
            self.show_features()
            self.quick_demo()
            self.save_profile()
            self.final_message()
            
            console.print("\n[bold green]✅ Onboarding complete![/bold green]")
            console.print("[dim]Press Enter to continue...[/dim]")
            input()
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Onboarding interrupted. Run 'jarvis onboard' to continue later.[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            sys.exit(1)


def main():
    """Main entry point"""
    onboarding = JarvisOnboarding()
    onboarding.run()


if __name__ == "__main__":
    main()
