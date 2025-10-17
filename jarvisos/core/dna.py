"""
JarvisOS User DNA Profiler
Creates unique genetic profile for each user
"""

import json
from pathlib import Path
from datetime import datetime, time
from typing import Dict, List, Optional
from collections import Counter, defaultdict

from ..utils.logger import get_logger

logger = get_logger("jarvisos.dna")


class UserDNA:
    """Represents user's unique computing DNA"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.dna_file = self.data_dir / "user_dna.json"
        
        self.profile = {
            'user_id': None,
            'name': None,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            
            # Chronotype
            'chronotype': {
                'type': None,  # morning, afternoon, evening, night
                'peak_hours': [],
                'low_hours': []
            },
            
            # Work patterns
            'work_patterns': {
                'typical_start': None,
                'typical_end': None,
                'focus_duration_avg': 0,
                'break_frequency': 0,
                'productive_days': []
            },
            
            # Tool preferences
            'tool_preferences': {
                'primary_apps': [],
                'editor': None,
                'browser': None,
                'terminal': None,
                'communication': []
            },
            
            # Workflow signatures
            'workflow_signatures': {
                'morning_routine': [],
                'work_routine': [],
                'evening_routine': [],
                'common_sequences': []
            },
            
            # Productivity rhythms
            'productivity_rhythms': {
                'best_hours': [],
                'worst_hours': [],
                'optimal_session_length': 0,
                'distraction_triggers': []
            },
            
            # Behavioral traits
            'traits': {
                'multitasker': False,
                'deep_focus': False,
                'frequent_switcher': False,
                'organized': False,
                'spontaneous': False
            },
            
            # Preferences
            'preferences': {
                'automation_level': 'medium',  # low, medium, high
                'notification_tolerance': 'medium',
                'privacy_level': 'high',
                'learning_speed': 'medium'
            }
        }
        
        self.load_profile()
        logger.info("UserDNA initialized")
    
    def load_profile(self):
        """Load existing DNA profile"""
        if self.dna_file.exists():
            try:
                with open(self.dna_file) as f:
                    saved_profile = json.load(f)
                    self.profile.update(saved_profile)
                logger.info("DNA profile loaded")
            except Exception as e:
                logger.error(f"Failed to load DNA profile: {e}")
    
    def save_profile(self):
        """Save DNA profile"""
        self.profile['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.dna_file, 'w') as f:
                json.dump(self.profile, f, indent=2)
            logger.info("DNA profile saved")
        except Exception as e:
            logger.error(f"Failed to save DNA profile: {e}")
    
    def analyze_observations(self, observations_data: Dict):
        """Analyze observations to build DNA profile"""
        logger.info("Analyzing observations for DNA profiling...")
        
        observations = observations_data.get('observations', [])
        if not observations:
            logger.warning("No observations to analyze")
            return
        
        # Analyze chronotype
        self._analyze_chronotype(observations)
        
        # Analyze work patterns
        self._analyze_work_patterns(observations)
        
        # Analyze tool preferences
        self._analyze_tool_preferences(observations)
        
        # Analyze workflow signatures
        self._analyze_workflow_signatures(observations)
        
        # Analyze productivity rhythms
        self._analyze_productivity_rhythms(observations)
        
        # Infer behavioral traits
        self._infer_traits(observations)
        
        self.save_profile()
        logger.info("DNA profile updated")
    
    def _analyze_chronotype(self, observations: List[Dict]):
        """Determine user's chronotype (morning/night person)"""
        hour_activity = defaultdict(int)
        
        for obs in observations:
            timestamp = datetime.fromisoformat(obs['timestamp'])
            hour = timestamp.hour
            hour_activity[hour] += len(obs.get('apps', []))
        
        if not hour_activity:
            return
        
        # Find peak hours
        sorted_hours = sorted(hour_activity.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [h for h, _ in sorted_hours[:4]]
        
        # Determine chronotype
        avg_peak_hour = sum(peak_hours) / len(peak_hours)
        
        if avg_peak_hour < 12:
            chronotype = 'morning'
        elif avg_peak_hour < 17:
            chronotype = 'afternoon'
        elif avg_peak_hour < 22:
            chronotype = 'evening'
        else:
            chronotype = 'night'
        
        self.profile['chronotype']['type'] = chronotype
        self.profile['chronotype']['peak_hours'] = peak_hours
        
        logger.debug(f"Chronotype detected: {chronotype}")
    
    def _analyze_work_patterns(self, observations: List[Dict]):
        """Analyze work patterns and schedule"""
        work_hours = []
        
        for obs in observations:
            timestamp = datetime.fromisoformat(obs['timestamp'])
            if len(obs.get('apps', [])) > 5:  # Active work
                work_hours.append(timestamp.hour)
        
        if work_hours:
            self.profile['work_patterns']['typical_start'] = min(work_hours)
            self.profile['work_patterns']['typical_end'] = max(work_hours)
            
            logger.debug(f"Work hours: {min(work_hours)}:00 - {max(work_hours)}:00")
    
    def _analyze_tool_preferences(self, observations: List[Dict]):
        """Identify preferred tools and applications"""
        app_counter = Counter()
        
        for obs in observations:
            for app in obs.get('apps', []):
                app_counter[app['name']] += 1
        
        # Top 10 apps
        top_apps = [app for app, _ in app_counter.most_common(10)]
        self.profile['tool_preferences']['primary_apps'] = top_apps
        
        # Identify specific tools
        for app in top_apps:
            app_lower = app.lower()
            if any(editor in app_lower for editor in ['code', 'vim', 'emacs', 'sublime', 'atom']):
                self.profile['tool_preferences']['editor'] = app
            elif any(browser in app_lower for browser in ['chrome', 'firefox', 'safari', 'edge']):
                self.profile['tool_preferences']['browser'] = app
            elif 'terminal' in app_lower or 'iterm' in app_lower:
                self.profile['tool_preferences']['terminal'] = app
        
        logger.debug(f"Primary apps: {top_apps[:5]}")
    
    def _analyze_workflow_signatures(self, observations: List[Dict]):
        """Identify common workflow patterns"""
        # Group observations by time of day
        morning_apps = []
        work_apps = []
        evening_apps = []
        
        for obs in observations:
            timestamp = datetime.fromisoformat(obs['timestamp'])
            hour = timestamp.hour
            apps = [app['name'] for app in obs.get('apps', [])]
            
            if 6 <= hour < 12:
                morning_apps.extend(apps)
            elif 12 <= hour < 18:
                work_apps.extend(apps)
            elif 18 <= hour < 24:
                evening_apps.extend(apps)
        
        # Find most common apps per period
        if morning_apps:
            morning_counter = Counter(morning_apps)
            self.profile['workflow_signatures']['morning_routine'] = [
                app for app, _ in morning_counter.most_common(5)
            ]
        
        if work_apps:
            work_counter = Counter(work_apps)
            self.profile['workflow_signatures']['work_routine'] = [
                app for app, _ in work_counter.most_common(5)
            ]
        
        if evening_apps:
            evening_counter = Counter(evening_apps)
            self.profile['workflow_signatures']['evening_routine'] = [
                app for app, _ in evening_counter.most_common(5)
            ]
        
        logger.debug("Workflow signatures identified")
    
    def _analyze_productivity_rhythms(self, observations: List[Dict]):
        """Analyze productivity patterns"""
        hour_productivity = defaultdict(list)
        
        for obs in observations:
            timestamp = datetime.fromisoformat(obs['timestamp'])
            hour = timestamp.hour
            
            # Productivity proxy: number of active apps
            productivity = len(obs.get('apps', []))
            hour_productivity[hour].append(productivity)
        
        # Calculate average productivity per hour
        hour_avg = {
            hour: sum(values) / len(values)
            for hour, values in hour_productivity.items()
        }
        
        if hour_avg:
            sorted_hours = sorted(hour_avg.items(), key=lambda x: x[1], reverse=True)
            
            self.profile['productivity_rhythms']['best_hours'] = [
                h for h, _ in sorted_hours[:3]
            ]
            self.profile['productivity_rhythms']['worst_hours'] = [
                h for h, _ in sorted_hours[-3:]
            ]
            
            logger.debug(f"Best hours: {self.profile['productivity_rhythms']['best_hours']}")
    
    def _infer_traits(self, observations: List[Dict]):
        """Infer behavioral traits from patterns"""
        total_apps = []
        app_switches = 0
        
        for i, obs in enumerate(observations):
            apps = obs.get('apps', [])
            total_apps.append(len(apps))
            
            if i > 0:
                prev_apps = set(a['name'] for a in observations[i-1].get('apps', []))
                curr_apps = set(a['name'] for a in apps)
                if prev_apps != curr_apps:
                    app_switches += 1
        
        if total_apps:
            avg_apps = sum(total_apps) / len(total_apps)
            switch_rate = app_switches / len(observations) if observations else 0
            
            # Infer traits
            self.profile['traits']['multitasker'] = avg_apps > 10
            self.profile['traits']['deep_focus'] = avg_apps < 5
            self.profile['traits']['frequent_switcher'] = switch_rate > 0.5
            
            logger.debug(f"Traits inferred: multitasker={self.profile['traits']['multitasker']}")
    
    def get_profile_summary(self) -> Dict:
        """Get human-readable profile summary"""
        return {
            'chronotype': self.profile['chronotype']['type'],
            'work_hours': f"{self.profile['work_patterns']['typical_start']}:00 - {self.profile['work_patterns']['typical_end']}:00",
            'primary_apps': self.profile['tool_preferences']['primary_apps'][:5],
            'best_hours': self.profile['productivity_rhythms']['best_hours'],
            'traits': [k for k, v in self.profile['traits'].items() if v]
        }
    
    def display_profile(self):
        """Display profile in console"""
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        console.print("\n[bold cyan]🧬 YOUR COMPUTING DNA[/bold cyan]\n")
        
        # Chronotype
        chronotype = self.profile['chronotype']['type']
        if chronotype:
            console.print(f"[yellow]Chronotype:[/yellow] {chronotype.title()} person")
            console.print(f"[dim]Peak hours: {self.profile['chronotype']['peak_hours']}[/dim]\n")
        
        # Work patterns
        start = self.profile['work_patterns']['typical_start']
        end = self.profile['work_patterns']['typical_end']
        if start and end:
            console.print(f"[yellow]Work Schedule:[/yellow] {start}:00 - {end}:00\n")
        
        # Primary apps
        apps = self.profile['tool_preferences']['primary_apps']
        if apps:
            console.print("[yellow]Primary Apps:[/yellow]")
            for i, app in enumerate(apps[:5], 1):
                console.print(f"  {i}. {app}")
            console.print()
        
        # Traits
        traits = [k.replace('_', ' ').title() for k, v in self.profile['traits'].items() if v]
        if traits:
            console.print(f"[yellow]Traits:[/yellow] {', '.join(traits)}\n")
        
        # Best hours
        best_hours = self.profile['productivity_rhythms']['best_hours']
        if best_hours:
            console.print(f"[yellow]Most Productive:[/yellow] {best_hours}:00\n")


# Example usage
if __name__ == "__main__":
    dna = UserDNA()
    
    # Load observations
    from pathlib import Path
    obs_file = Path("data/observations.json")
    if obs_file.exists():
        with open(obs_file) as f:
            observations_data = json.load(f)
        
        dna.analyze_observations(observations_data)
        dna.display_profile()
