"""
JarvisOS Context Awareness System
Understands what the user is doing and adapts behavior
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import Counter

from ..utils.logger import get_logger

logger = get_logger("jarvisos.context")


class ContextType:
    """Context types"""
    FOCUS = "focus"           # Deep work, coding, writing
    MEETING = "meeting"       # Video call, presentation
    BROWSING = "browsing"     # Web research, reading
    COMMUNICATION = "communication"  # Email, chat, messaging
    IDLE = "idle"             # No activity
    BREAK = "break"           # Short break
    UNKNOWN = "unknown"


class ContextAnalyzer:
    """Analyzes user context from observations"""
    
    # App patterns for context detection
    FOCUS_APPS = {
        'vscode', 'code', 'pycharm', 'intellij', 'sublime', 'vim', 'emacs',
        'xcode', 'android studio', 'visual studio', 'atom', 'notepad++',
        'word', 'pages', 'libreoffice', 'writer', 'photoshop', 'illustrator',
        'figma', 'sketch', 'blender', 'unity', 'unreal'
    }
    
    MEETING_APPS = {
        'zoom', 'teams', 'meet', 'skype', 'webex', 'slack call',
        'discord', 'facetime', 'google meet', 'microsoft teams'
    }
    
    BROWSING_APPS = {
        'chrome', 'firefox', 'safari', 'edge', 'brave', 'opera'
    }
    
    COMMUNICATION_APPS = {
        'slack', 'discord', 'telegram', 'whatsapp', 'signal',
        'mail', 'outlook', 'thunderbird', 'gmail', 'messages'
    }
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.context_file = self.data_dir / "context_history.json"
        self.current_context_file = self.data_dir / "current_context.json"
        
        logger.info("ContextAnalyzer initialized")
    
    def detect_context(self, observation: Dict) -> str:
        """Detect context from single observation"""
        processes = observation.get('processes', [])
        
        if not processes:
            return ContextType.IDLE
        
        # Get top apps by CPU usage
        top_apps = sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:3]
        app_names = [app['name'].lower() for app in top_apps]
        
        # Check for focus apps
        if any(app in self.FOCUS_APPS for app in app_names):
            # High CPU usage = active work
            top_cpu = top_apps[0].get('cpu_percent', 0)
            if top_cpu > 20:
                return ContextType.FOCUS
        
        # Check for meetings
        if any(app in self.MEETING_APPS for app in app_names):
            return ContextType.MEETING
        
        # Check for communication
        if any(app in self.COMMUNICATION_APPS for app in app_names):
            return ContextType.COMMUNICATION
        
        # Check for browsing
        if any(app in self.BROWSING_APPS for app in app_names):
            # Low CPU = reading, high CPU = active browsing
            top_cpu = top_apps[0].get('cpu_percent', 0)
            if top_cpu < 10:
                return ContextType.BROWSING
        
        # Check for idle
        total_cpu = sum(p.get('cpu_percent', 0) for p in processes)
        if total_cpu < 5:
            return ContextType.IDLE
        
        return ContextType.UNKNOWN
    
    def analyze_session(self, observations: List[Dict]) -> Dict:
        """Analyze a session of observations"""
        if not observations:
            return {
                'dominant_context': ContextType.UNKNOWN,
                'contexts': {},
                'focus_time': 0,
                'break_time': 0,
                'productive': False
            }
        
        # Detect context for each observation
        contexts = [self.detect_context(obs) for obs in observations]
        context_counts = Counter(contexts)
        
        # Calculate time in each context (assuming 5 min intervals)
        interval_minutes = 5
        context_times = {
            ctx: count * interval_minutes 
            for ctx, count in context_counts.items()
        }
        
        # Determine dominant context
        dominant = context_counts.most_common(1)[0][0] if contexts else ContextType.UNKNOWN
        
        # Calculate focus time
        focus_time = context_times.get(ContextType.FOCUS, 0)
        
        # Calculate break time
        break_time = context_times.get(ContextType.IDLE, 0) + context_times.get(ContextType.BREAK, 0)
        
        # Determine if productive
        productive_contexts = {ContextType.FOCUS, ContextType.MEETING, ContextType.COMMUNICATION}
        productive_time = sum(
            context_times.get(ctx, 0) 
            for ctx in productive_contexts
        )
        total_time = sum(context_times.values())
        productive = (productive_time / total_time > 0.6) if total_time > 0 else False
        
        return {
            'dominant_context': dominant,
            'contexts': dict(context_counts),
            'context_times': context_times,
            'focus_time': focus_time,
            'break_time': break_time,
            'productive': productive,
            'total_time': total_time
        }
    
    def get_current_context(self) -> Optional[Dict]:
        """Get current context"""
        if not self.current_context_file.exists():
            return None
        
        try:
            with open(self.current_context_file) as f:
                return json.load(f)
        except:
            return None
    
    def save_current_context(self, context: str, metadata: Dict = None):
        """Save current context"""
        data = {
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        with open(self.current_context_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Current context saved: {context}")
    
    def should_interrupt(self) -> bool:
        """Check if it's OK to interrupt user"""
        current = self.get_current_context()
        
        if not current:
            return True  # No context info, assume OK
        
        context = current.get('context')
        timestamp = current.get('timestamp')
        
        # Never interrupt during focus or meeting
        if context in [ContextType.FOCUS, ContextType.MEETING]:
            return False
        
        # OK to interrupt during breaks or idle
        if context in [ContextType.IDLE, ContextType.BREAK]:
            return True
        
        # Check if context is stale (> 30 min old)
        if timestamp:
            try:
                ctx_time = datetime.fromisoformat(timestamp)
                if datetime.now() - ctx_time > timedelta(minutes=30):
                    return True  # Stale, assume OK
            except:
                pass
        
        # Default: OK to interrupt for other contexts
        return True
    
    def detect_focus_session(self, observations: List[Dict]) -> Optional[Dict]:
        """Detect if user is in a focus session"""
        if len(observations) < 3:
            return None
        
        # Check last 3 observations (15 min)
        recent = observations[-3:]
        contexts = [self.detect_context(obs) for obs in recent]
        
        # All focus = focus session
        if all(ctx == ContextType.FOCUS for ctx in contexts):
            # Calculate duration
            start_time = recent[0].get('timestamp')
            duration_minutes = len(recent) * 5
            
            return {
                'in_focus': True,
                'duration_minutes': duration_minutes,
                'start_time': start_time
            }
        
        return None
    
    def get_best_notification_time(self) -> str:
        """Suggest best time for notifications based on patterns"""
        # Load context history
        if not self.context_file.exists():
            return "09:00"  # Default morning
        
        try:
            with open(self.context_file) as f:
                history = json.load(f)
            
            # Find times when user is typically in IDLE or BREAK
            # This is simplified - real implementation would analyze patterns
            return "09:00"  # Morning is usually good
        except:
            return "09:00"
    
    def save_context_history(self, session_analysis: Dict):
        """Save context analysis to history"""
        history = []
        
        if self.context_file.exists():
            try:
                with open(self.context_file) as f:
                    history = json.load(f)
            except:
                history = []
        
        # Add new entry
        entry = {
            'timestamp': datetime.now().isoformat(),
            **session_analysis
        }
        history.append(entry)
        
        # Keep last 100 entries
        history = history[-100:]
        
        with open(self.context_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        logger.info("Context history saved")


class SmartInterruptionManager:
    """Manages when to interrupt user based on context"""
    
    def __init__(self):
        self.context_analyzer = ContextAnalyzer()
    
    def can_notify(self, priority: str = "normal") -> bool:
        """Check if we can send notification"""
        # High priority always goes through
        if priority == "high":
            return True
        
        # Check context
        if not self.context_analyzer.should_interrupt():
            logger.info("Notification blocked: User in focus/meeting")
            return False
        
        return True
    
    def queue_notification(self, message: str, priority: str = "normal"):
        """Queue notification for later if can't send now"""
        if self.can_notify(priority):
            return True  # Send now
        
        # Queue for later
        queue_file = Path("data/notification_queue.json")
        queue = []
        
        if queue_file.exists():
            try:
                with open(queue_file) as f:
                    queue = json.load(f)
            except:
                queue = []
        
        queue.append({
            'message': message,
            'priority': priority,
            'queued_at': datetime.now().isoformat()
        })
        
        with open(queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        logger.info(f"Notification queued: {message[:50]}...")
        return False  # Queued, not sent


# CLI function
def analyze_current_context():
    """Analyze current context from latest observations"""
    from .observer import Observer
    
    analyzer = ContextAnalyzer()
    
    # Load recent observations
    obs_file = Path("data/observations.json")
    if not obs_file.exists():
        print("No observations found. Run 'jarvis observe' first.")
        return
    
    with open(obs_file) as f:
        data = json.load(f)
    
    observations = data.get('observations', [])
    
    if not observations:
        print("No observations to analyze.")
        return
    
    # Analyze last observation
    latest = observations[-1]
    context = analyzer.detect_context(latest)
    
    print(f"\n🧠 Current Context: {context}")
    
    # Analyze recent session (last hour = 12 observations)
    recent = observations[-12:] if len(observations) >= 12 else observations
    session = analyzer.analyze_session(recent)
    
    print(f"\n📊 Session Analysis:")
    print(f"  Dominant: {session['dominant_context']}")
    print(f"  Focus Time: {session['focus_time']} min")
    print(f"  Productive: {'Yes' if session['productive'] else 'No'}")
    
    # Check if can interrupt
    can_interrupt = analyzer.should_interrupt()
    print(f"\n🔔 Can Interrupt: {'Yes' if can_interrupt else 'No (in focus/meeting)'}")


if __name__ == "__main__":
    analyze_current_context()
