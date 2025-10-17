"""
JarvisOS User Feedback System
Allows users to rate scripts and provide feedback
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from ..utils.logger import get_logger

logger = get_logger("jarvisos.feedback")
console = Console()


class FeedbackManager:
    """Manages user feedback for scripts and automations"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.feedback_file = self.data_dir / "feedback.json"
        
        logger.info("FeedbackManager initialized")
    
    def load_feedback(self) -> Dict:
        """Load all feedback"""
        if not self.feedback_file.exists():
            return {}
        
        try:
            with open(self.feedback_file) as f:
                return json.load(f)
        except:
            return {}
    
    def save_feedback(self, feedback: Dict):
        """Save feedback"""
        with open(self.feedback_file, 'w') as f:
            json.dump(feedback, f, indent=2)
        
        logger.info("Feedback saved")
    
    def rate_script(self, script_id: str, rating: int, comment: str = ""):
        """Rate a script (1-5 stars)"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        feedback = self.load_feedback()
        
        if script_id not in feedback:
            feedback[script_id] = {
                'ratings': [],
                'comments': [],
                'average_rating': 0.0
            }
        
        # Add rating
        feedback[script_id]['ratings'].append({
            'rating': rating,
            'timestamp': datetime.now().isoformat(),
            'comment': comment
        })
        
        # Update average
        ratings = [r['rating'] for r in feedback[script_id]['ratings']]
        feedback[script_id]['average_rating'] = sum(ratings) / len(ratings)
        
        self.save_feedback(feedback)
        
        logger.info(f"Script {script_id} rated: {rating}/5")
        
        return feedback[script_id]
    
    def thumbs_up(self, script_id: str, comment: str = ""):
        """Quick thumbs up (5 stars)"""
        return self.rate_script(script_id, 5, comment)
    
    def thumbs_down(self, script_id: str, comment: str = ""):
        """Quick thumbs down (1 star)"""
        return self.rate_script(script_id, 1, comment)
    
    def get_script_rating(self, script_id: str) -> Optional[float]:
        """Get average rating for script"""
        feedback = self.load_feedback()
        
        if script_id not in feedback:
            return None
        
        return feedback[script_id].get('average_rating', 0.0)
    
    def get_top_rated_scripts(self, n: int = 5) -> List[Dict]:
        """Get top rated scripts"""
        feedback = self.load_feedback()
        
        # Sort by average rating
        sorted_scripts = sorted(
            feedback.items(),
            key=lambda x: x[1].get('average_rating', 0),
            reverse=True
        )
        
        return [
            {
                'script_id': script_id,
                'rating': data['average_rating'],
                'num_ratings': len(data['ratings'])
            }
            for script_id, data in sorted_scripts[:n]
        ]
    
    def get_feedback_summary(self) -> Dict:
        """Get feedback summary"""
        feedback = self.load_feedback()
        
        total_scripts = len(feedback)
        total_ratings = sum(len(data['ratings']) for data in feedback.values())
        
        if total_ratings == 0:
            return {
                'total_scripts': 0,
                'total_ratings': 0,
                'average_rating': 0.0
            }
        
        # Calculate overall average
        all_ratings = []
        for data in feedback.values():
            all_ratings.extend([r['rating'] for r in data['ratings']])
        
        average = sum(all_ratings) / len(all_ratings)
        
        return {
            'total_scripts': total_scripts,
            'total_ratings': total_ratings,
            'average_rating': round(average, 2)
        }
    
    def prompt_for_feedback(self, script_id: str, script_name: str):
        """Interactively prompt user for feedback"""
        console.print(f"\n[bold cyan]📝 Feedback for: {script_name}[/bold cyan]\n")
        
        # Quick rating
        console.print("[yellow]How would you rate this script?[/yellow]")
        console.print("  👍 Thumbs up (great!)")
        console.print("  👎 Thumbs down (not helpful)")
        console.print("  ⭐ Custom rating (1-5 stars)")
        console.print()
        
        choice = Prompt.ask(
            "Your choice",
            choices=["up", "down", "custom", "skip"],
            default="skip"
        )
        
        if choice == "skip":
            console.print("[dim]Skipped[/dim]\n")
            return None
        
        if choice == "up":
            rating = 5
            console.print("[green]👍 Thanks![/green]")
        elif choice == "down":
            rating = 1
            console.print("[red]👎 Got it, we'll improve.[/red]")
        else:
            rating = int(Prompt.ask(
                "Rating (1-5)",
                choices=["1", "2", "3", "4", "5"],
                default="3"
            ))
        
        # Optional comment
        add_comment = Confirm.ask("Add a comment?", default=False)
        comment = ""
        
        if add_comment:
            comment = Prompt.ask("Comment")
        
        # Save feedback
        result = self.rate_script(script_id, rating, comment)
        
        console.print(f"\n[green]✅ Feedback saved! Average: {result['average_rating']:.1f}/5[/green]\n")
        
        return result
    
    def display_feedback_summary(self):
        """Display feedback summary"""
        summary = self.get_feedback_summary()
        
        panel = Panel(
            f"[bold cyan]Total Scripts Rated:[/bold cyan] {summary['total_scripts']}\n"
            f"[bold cyan]Total Ratings:[/bold cyan] {summary['total_ratings']}\n"
            f"[bold cyan]Average Rating:[/bold cyan] {summary['average_rating']}/5 ⭐",
            title="[bold]Feedback Summary[/bold]",
            border_style="cyan"
        )
        
        console.print(panel)
        
        # Show top rated
        top = self.get_top_rated_scripts(5)
        
        if top:
            console.print("\n[bold]🏆 Top Rated Scripts:[/bold]\n")
            
            table = Table()
            table.add_column("Script ID", style="cyan")
            table.add_column("Rating", style="yellow")
            table.add_column("# Ratings", style="dim")
            
            for script in top:
                table.add_row(
                    script['script_id'],
                    f"{script['rating']:.1f} ⭐",
                    str(script['num_ratings'])
                )
            
            console.print(table)
            console.print()


class FeedbackIntegration:
    """Integrates feedback with gene fitness"""
    
    def __init__(self):
        self.feedback_manager = FeedbackManager()
    
    def update_gene_fitness_from_feedback(self, gene_id: str) -> Optional[float]:
        """Update gene fitness based on user feedback"""
        rating = self.feedback_manager.get_script_rating(gene_id)
        
        if rating is None:
            return None
        
        # Convert rating (1-5) to fitness boost (0-1)
        # 5 stars = +0.5 fitness
        # 1 star = -0.5 fitness
        fitness_boost = (rating - 3) / 4  # Maps 1-5 to -0.5 to +0.5
        
        logger.info(f"Gene {gene_id} fitness boost from feedback: {fitness_boost:+.2f}")
        
        return fitness_boost
    
    def get_all_feedback_boosts(self) -> Dict[str, float]:
        """Get fitness boosts for all genes"""
        feedback = self.feedback_manager.load_feedback()
        
        boosts = {}
        for gene_id, data in feedback.items():
            rating = data.get('average_rating', 3.0)
            boosts[gene_id] = (rating - 3) / 4
        
        return boosts


# CLI functions
def rate_script_cli(script_id: str):
    """Rate a script from CLI"""
    manager = FeedbackManager()
    manager.prompt_for_feedback(script_id, script_id)


def show_feedback_cli():
    """Show feedback summary from CLI"""
    manager = FeedbackManager()
    manager.display_feedback_summary()


if __name__ == "__main__":
    show_feedback_cli()
