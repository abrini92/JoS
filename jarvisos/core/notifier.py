"""
JarvisOS Proactive Notification System
Makes Jarvis speak when he has something to say
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel

from ..voice.jarvis_voice import JarvisVoice
from ..utils.logger import get_logger
from .personality import JarvisPersonality
from .context import ContextAnalyzer

# Native notifications
try:
    from ..ui.native_notifications import notify_jarvis, notify_success, notify_info
    NATIVE_NOTIFICATIONS = True
except ImportError:
    NATIVE_NOTIFICATIONS = False
    logger = get_logger("jarvisos.notifier")
console = Console()


class ProactiveNotifier:
    """Manages proactive notifications and voice announcements"""
    
    def __init__(self, data_dir: str = "data", use_voice: bool = True):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.insights_file = self.data_dir / "insights.json"
        self.notifications_file = self.data_dir / "notifications.json"
        self.last_notify_file = self.data_dir / "last_notification.json"
        
        self.use_voice = use_voice
        self.jarvis = JarvisVoice() if use_voice else None
        
        logger.info("ProactiveNotifier initialized")
    
    def should_notify(self) -> bool:
        """Check if we should notify user (not too frequent)"""
        if not self.last_notify_file.exists():
            return True
        
        try:
            with open(self.last_notify_file) as f:
                data = json.load(f)
            
            last_time = datetime.fromisoformat(data['timestamp'])
            
            # Don't notify more than once per hour
            if datetime.now() - last_time < timedelta(hours=1):
                return False
            
            return True
        except:
            return True
    
    def mark_notified(self):
        """Mark that we just notified"""
        data = {
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.last_notify_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_for_insights(self) -> bool:
        """Check if there are new insights to share"""
        if not self.insights_file.exists():
            return False
        
        try:
            with open(self.insights_file) as f:
                insights = json.load(f)
            
            # Check if insights are recent (within last 24h)
            if 'timestamp' in insights:
                insight_time = datetime.fromisoformat(insights['timestamp'])
                if datetime.now() - insight_time < timedelta(hours=24):
                    return True
            
            return False
        except:
            return False
    
    def notify_insights_ready(self):
        """Notify user that insights are ready"""
        if not self.should_notify():
            logger.info("Skipping notification (too soon)")
            return
        
        console.print("\n")
        
        # Use personality for intro
        intro = JarvisPersonality.introduce_insight()
        
        panel = Panel(
            f"[bold cyan]✨ {intro}[/bold cyan]\n\n"
            "[yellow]I've completed my analysis and discovered some fascinating patterns "
            "in your workflow.[/yellow]\n\n"
            "[green]I think you're going to find this quite valuable![/green]\n\n"
            "[dim]Run 'jarvis summary' when you're ready to see what I've learned.[/dim]",
            border_style="cyan",
            padding=(1, 2),
            title="[bold]Jarvis[/bold]"
        )
        
        console.print(panel)
        console.print("\n")
        
        # Native notification
        if NATIVE_NOTIFICATIONS:
            notify_jarvis(
                "I've completed my analysis!",
                subtitle="Insights Ready",
                actions=["View", "Later"]
            )
        
        if self.jarvis:
            message = (
                f"{intro} "
                "I've completed my analysis and found some fascinating patterns. "
                "I think you're going to find this quite valuable. "
                "Run jarvis summary when you're ready."
            )
            self.jarvis.speak(message)
        
        self.mark_notified()
        logger.info("Insights notification sent")
    
    def notify_scripts_generated(self, count: int):
        """Notify user that scripts were generated"""
        if not self.should_notify():
            return
        
        console.print("\n")
        
        # Celebrate!
        celebration = JarvisPersonality.celebrate()
        
        panel = Panel(
            f"[bold green]🎉 {celebration}[/bold green]\n\n"
            f"[yellow]I've created {count} custom automation script{'s' if count > 1 else ''} "
            f"tailored specifically to your workflow.[/yellow]\n\n"
            "[green]I think these are going to save you significant time![/green]\n\n"
            "[dim]Run 'jarvis list' to see them.[/dim]",
            border_style="green",
            padding=(1, 2),
            title="[bold]Jarvis[/bold]"
        )
        
        console.print(panel)
        console.print("\n")
        
        if self.jarvis:
            message = (
                f"{celebration} "
                f"I've created {count} custom automation script{'s' if count > 1 else ''} for you. "
                "I think these are going to save you significant time. "
                "Run jarvis list to see them."
            )
            self.jarvis.speak(message)
        
        self.mark_notified()
        logger.info(f"Scripts notification sent: {count} scripts")
    
    def notify_evolution_complete(self, stats: Dict):
        """Notify user that evolution cycle completed"""
        if not self.should_notify():
            return
        
        console.print("\n")
        
        mutations = stats.get('mutations_created', 0)
        selected = stats.get('genes_selected', 0)
        
        panel = Panel(
            "[bold magenta]🧬 EVOLUTION CYCLE COMPLETE[/bold magenta]\n\n"
            f"[yellow]Selected: {selected} top genes[/yellow]\n"
            f"[yellow]Mutations: {mutations} new variants created[/yellow]\n\n"
            "[dim]Your system is evolving![/dim]",
            border_style="magenta",
            padding=(1, 2)
        )
        
        console.print(panel)
        console.print("\n")
        
        if self.jarvis:
            message = (
                f"Evolution cycle complete! "
                f"I selected {selected} top performing scripts and created {mutations} new variants. "
                "Your system is getting better."
            )
            self.jarvis.speak(message)
        
        self.mark_notified()
        logger.info("Evolution notification sent")
    
    def morning_greeting(self, user_name: str = "there"):
        """Morning greeting with daily summary"""
        console.print("\n")
        
        # Use personality for greeting
        greeting = JarvisPersonality.greet()
        
        panel = Panel(
            f"[bold cyan]{greeting}[/bold cyan]\n\n"
            f"[yellow]Hello, {user_name}! I'm ready to help you accomplish great things today.[/yellow]\n\n"
            "[green]I'm here whenever you need me.[/green]\n\n"
            "[dim]Type 'jarvis status' to see what I'm working on.[/dim]",
            border_style="cyan",
            padding=(1, 2),
            title="[bold]Jarvis[/bold]"
        )
        
        console.print(panel)
        console.print("\n")
        
        if self.jarvis:
            message = f"{greeting} I'm ready to help you accomplish great things today."
            self.jarvis.speak(message)
        
        logger.info(f"Morning greeting sent to {user_name}")
    
    def notify_observation_milestone(self, count: int):
        """Notify when observation milestone reached"""
        milestones = [10, 50, 100, 500, 1000]
        
        if count not in milestones:
            return
        
        if not self.should_notify():
            return
        
        console.print("\n")
        
        panel = Panel(
            f"[bold cyan]📊 MILESTONE: {count} OBSERVATIONS COLLECTED[/bold cyan]\n\n"
            "[yellow]I'm learning more about you every day.[/yellow]\n\n"
            "[dim]The more data I have, the better I can help you.[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(panel)
        console.print("\n")
        
        if self.jarvis:
            message = (
                f"Milestone reached! I've collected {count} observations. "
                "I'm learning more about your workflow every day."
            )
            self.jarvis.speak(message)
        
        self.mark_notified()
        logger.info(f"Milestone notification sent: {count} observations")
    
    def check_and_notify(self):
        """Check for any pending notifications and send them"""
        logger.info("Checking for pending notifications...")
        
        # Check for insights
        if self.check_for_insights():
            self.notify_insights_ready()
            return True
        
        return False


# CLI function
def check_notifications():
    """Check and send notifications (called by cron/timer)"""
    notifier = ProactiveNotifier()
    notifier.check_and_notify()


if __name__ == "__main__":
    check_notifications()
