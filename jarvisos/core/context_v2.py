#!/usr/bin/env python3
"""
JarvisOS - Multi-Dimensional Context System V2
Top 0.1% - Legendary Intelligence

Provides deep, multi-dimensional understanding of user context.
Not just "what" but "why" and "what's next".
"""

import json
import psutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import subprocess


@dataclass
class TemporalContext:
    """Time-based context"""
    time: str
    hour: int
    minute: int
    day: str
    day_of_week: int
    week: int
    month: str
    season: str
    is_holiday: bool
    is_weekend: bool
    time_of_day: str  # morning, afternoon, evening, night
    time_since_boot: int  # seconds
    time_since_last_action: int  # seconds
    
    @classmethod
    def capture(cls, last_action_time: Optional[float] = None):
        """Capture current temporal context"""
        now = datetime.now()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        # Determine time of day
        hour = now.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # Determine season (Northern Hemisphere)
        month = now.month
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "fall"
        
        return cls(
            time=now.strftime("%H:%M:%S"),
            hour=hour,
            minute=now.minute,
            day=now.strftime("%A"),
            day_of_week=now.weekday(),
            week=now.isocalendar()[1],
            month=now.strftime("%B"),
            season=season,
            is_holiday=False,  # TODO: Holiday detection
            is_weekend=now.weekday() >= 5,
            time_of_day=time_of_day,
            time_since_boot=int((now - boot_time).total_seconds()),
            time_since_last_action=int(time.time() - last_action_time) if last_action_time else 0
        )


@dataclass
class BehavioralContext:
    """User behavior patterns"""
    typing_speed: str  # slow, normal, fast
    mouse_activity: str  # low, medium, high
    app_switches: int
    focus_duration: int  # seconds
    break_pattern: str  # regular, irregular, none
    multitasking: bool
    
    @classmethod
    def capture(cls, observation_window: int = 300):
        """Capture behavioral context from recent activity"""
        # TODO: Implement actual behavior tracking
        # For now, return defaults
        return cls(
            typing_speed="normal",
            mouse_activity="medium",
            app_switches=0,
            focus_duration=0,
            break_pattern="regular",
            multitasking=False
        )


@dataclass
class EnvironmentalContext:
    """Physical environment context"""
    battery_level: int
    battery_plugged: bool
    network_type: str  # wifi, ethernet, cellular, none
    connected_devices: List[str]
    location: str  # home, office, mobile, unknown
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    
    @classmethod
    def capture(cls):
        """Capture environmental context"""
        battery = psutil.sensors_battery() if hasattr(psutil, 'sensors_battery') else None
        
        # Network detection
        net_io = psutil.net_io_counters()
        network_type = "wifi" if net_io.bytes_sent > 0 else "none"
        
        # Location inference (basic)
        # TODO: More sophisticated location detection
        location = "home" if battery and battery.power_plugged else "mobile"
        
        return cls(
            battery_level=int(battery.percent) if battery else 100,
            battery_plugged=battery.power_plugged if battery else True,
            network_type=network_type,
            connected_devices=[],  # TODO: Device detection
            location=location,
            cpu_usage=psutil.cpu_percent(interval=0.1),
            memory_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent
        )


@dataclass
class CognitiveContext:
    """Inferred cognitive state"""
    energy_level: str  # low, medium, high
    stress_level: str  # low, medium, high
    focus_quality: str  # poor, fair, good, excellent
    productivity_score: float  # 0-10
    
    @classmethod
    def infer(cls, temporal: TemporalContext, behavioral: BehavioralContext, 
              environmental: EnvironmentalContext):
        """Infer cognitive state from other contexts"""
        
        # Energy level inference
        if temporal.time_of_day == "morning" and temporal.hour < 10:
            energy_level = "high"
        elif temporal.time_of_day == "afternoon" and temporal.hour > 14:
            energy_level = "medium"
        elif temporal.time_of_day == "evening":
            energy_level = "low"
        else:
            energy_level = "medium"
        
        # Stress level inference
        if behavioral.app_switches > 20:
            stress_level = "high"
        elif behavioral.multitasking:
            stress_level = "medium"
        else:
            stress_level = "low"
        
        # Focus quality
        if behavioral.focus_duration > 1800:  # 30+ minutes
            focus_quality = "excellent"
        elif behavioral.focus_duration > 900:  # 15+ minutes
            focus_quality = "good"
        elif behavioral.focus_duration > 300:  # 5+ minutes
            focus_quality = "fair"
        else:
            focus_quality = "poor"
        
        # Productivity score (0-10)
        score = 5.0
        if energy_level == "high":
            score += 2
        if stress_level == "low":
            score += 1
        if focus_quality == "excellent":
            score += 2
        
        return cls(
            energy_level=energy_level,
            stress_level=stress_level,
            focus_quality=focus_quality,
            productivity_score=min(10.0, score)
        )


@dataclass
class SocialContext:
    """Social/collaboration context"""
    calendar_events: List[Dict[str, Any]]
    in_meeting: bool
    collaboration_mode: bool
    communication_urgency: str  # low, medium, high
    
    @classmethod
    def capture(cls):
        """Capture social context"""
        # TODO: Calendar integration
        # TODO: Communication app monitoring
        return cls(
            calendar_events=[],
            in_meeting=False,
            collaboration_mode=False,
            communication_urgency="low"
        )


@dataclass
class ProjectContext:
    """Current project/task context"""
    current_project: Optional[str]
    current_task: Optional[str]
    progress: float  # 0-100
    blockers: List[str]
    next_milestone: Optional[str]
    
    @classmethod
    def capture(cls, data_dir: Path):
        """Capture project context from user DNA"""
        # TODO: Read from user DNA and recent activity
        return cls(
            current_project=None,
            current_task=None,
            progress=0.0,
            blockers=[],
            next_milestone=None
        )


@dataclass
class MultiDimensionalContext:
    """Complete multi-dimensional context"""
    temporal: TemporalContext
    behavioral: BehavioralContext
    environmental: EnvironmentalContext
    cognitive: CognitiveContext
    social: SocialContext
    project: ProjectContext
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "temporal": asdict(self.temporal),
            "behavioral": asdict(self.behavioral),
            "environmental": asdict(self.environmental),
            "cognitive": asdict(self.cognitive),
            "social": asdict(self.social),
            "project": asdict(self.project),
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def capture_now(cls, data_dir: Path, last_action_time: Optional[float] = None):
        """Capture complete context right now"""
        temporal = TemporalContext.capture(last_action_time)
        behavioral = BehavioralContext.capture()
        environmental = EnvironmentalContext.capture()
        cognitive = CognitiveContext.infer(temporal, behavioral, environmental)
        social = SocialContext.capture()
        project = ProjectContext.capture(data_dir)
        
        return cls(
            temporal=temporal,
            behavioral=behavioral,
            environmental=environmental,
            cognitive=cognitive,
            social=social,
            project=project,
            timestamp=time.time()
        )


class ContextAnalyzer:
    """Analyzes and interprets multi-dimensional context"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.context_history: List[MultiDimensionalContext] = []
        self.last_action_time: Optional[float] = None
    
    def get_current_context(self) -> MultiDimensionalContext:
        """Get current multi-dimensional context"""
        context = MultiDimensionalContext.capture_now(
            self.data_dir,
            self.last_action_time
        )
        
        # Store in history
        self.context_history.append(context)
        
        # Keep only last 100 contexts
        if len(self.context_history) > 100:
            self.context_history = self.context_history[-100:]
        
        return context
    
    def update_last_action(self):
        """Update timestamp of last user action"""
        self.last_action_time = time.time()
    
    def get_context_summary(self) -> str:
        """Get human-readable context summary"""
        context = self.get_current_context()
        
        summary = f"""
Current Context:
  Time: {context.temporal.time_of_day} ({context.temporal.time})
  Day: {context.temporal.day}
  Energy: {context.cognitive.energy_level}
  Focus: {context.cognitive.focus_quality}
  Productivity: {context.cognitive.productivity_score:.1f}/10
  Location: {context.environmental.location}
  Battery: {context.environmental.battery_level}%
"""
        
        if context.project.current_project:
            summary += f"  Project: {context.project.current_project}\n"
        
        if context.social.in_meeting:
            summary += "  Status: In meeting\n"
        
        return summary.strip()
    
    def is_good_time_to_interrupt(self) -> bool:
        """Determine if it's a good time to interrupt user"""
        context = self.get_current_context()
        
        # Don't interrupt if:
        # - In a meeting
        if context.social.in_meeting:
            return False
        
        # - Deep focus (30+ minutes)
        if context.behavioral.focus_duration > 1800:
            return False
        
        # - High stress
        if context.cognitive.stress_level == "high":
            return False
        
        # - Low energy and not urgent
        if context.cognitive.energy_level == "low":
            return False
        
        return True
    
    def get_optimal_work_time(self) -> str:
        """Determine optimal time for focused work"""
        context = self.get_current_context()
        
        if context.cognitive.energy_level == "high" and context.cognitive.stress_level == "low":
            return "now"
        elif context.temporal.time_of_day == "morning":
            return "now"
        else:
            return "tomorrow morning"
    
    def save_context_history(self):
        """Save context history to file"""
        history_file = self.data_dir / "context_history.json"
        
        data = [ctx.to_dict() for ctx in self.context_history]
        
        with open(history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_context_history(self):
        """Load context history from file"""
        history_file = self.data_dir / "context_history.json"
        
        if not history_file.exists():
            return
        
        with open(history_file, 'r') as f:
            data = json.load(f)
        
        # TODO: Reconstruct MultiDimensionalContext objects
        # For now, just keep as dicts
        self.context_history = data


if __name__ == "__main__":
    # Test the context system
    from pathlib import Path
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    analyzer = ContextAnalyzer(data_dir)
    
    print("=== Multi-Dimensional Context System ===\n")
    
    context = analyzer.get_current_context()
    
    print("Temporal Context:")
    print(f"  Time: {context.temporal.time} ({context.temporal.time_of_day})")
    print(f"  Day: {context.temporal.day}")
    print(f"  Season: {context.temporal.season}")
    print()
    
    print("Environmental Context:")
    print(f"  Battery: {context.environmental.battery_level}%")
    print(f"  Location: {context.environmental.location}")
    print(f"  CPU: {context.environmental.cpu_usage:.1f}%")
    print(f"  Memory: {context.environmental.memory_usage:.1f}%")
    print()
    
    print("Cognitive Context:")
    print(f"  Energy: {context.cognitive.energy_level}")
    print(f"  Stress: {context.cognitive.stress_level}")
    print(f"  Focus: {context.cognitive.focus_quality}")
    print(f"  Productivity: {context.cognitive.productivity_score:.1f}/10")
    print()
    
    print("Summary:")
    print(analyzer.get_context_summary())
    print()
    
    print(f"Good time to interrupt? {analyzer.is_good_time_to_interrupt()}")
    print(f"Optimal work time: {analyzer.get_optimal_work_time()}")
