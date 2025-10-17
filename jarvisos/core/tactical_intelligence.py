#!/usr/bin/env python3
"""
JarvisOS - Tactical Intelligence Layer
Top 0.1% - Session planning and goal-oriented optimization

Not just next action - ENTIRE SESSION PLANNING
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

from .ai_brain import AIBrain
from .context_v2 import ContextAnalyzer


@dataclass
class SessionPhase:
    """A phase in a work session"""
    name: str
    duration_minutes: int
    actions: List[str]
    success_criteria: List[str]
    break_after: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SessionPlan:
    """A complete session plan"""
    goal: str
    estimated_duration_minutes: int
    optimal_start_time: str
    phases: List[SessionPhase]
    potential_blockers: List[str]
    success_criteria: List[str]
    created_at: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "optimal_start_time": self.optimal_start_time,
            "phases": [p.to_dict() for p in self.phases],
            "potential_blockers": self.potential_blockers,
            "success_criteria": self.success_criteria,
            "created_at": self.created_at
        }


class SessionPlanner:
    """
    Plans entire work sessions strategically
    
    Not just "what's next" but "how to achieve this goal optimally"
    """
    
    def __init__(self, ai_brain: AIBrain):
        self.ai_brain = ai_brain
        self.active_plan: Optional[SessionPlan] = None
        self.plan_history: List[SessionPlan] = []
    
    def create_session_plan(self, user_goal: str) -> SessionPlan:
        """
        Create a comprehensive session plan for a goal
        
        Uses AI to strategically plan the entire session
        """
        
        # Get AI's strategic plan
        ai_plan = self.ai_brain.plan_session(user_goal)
        
        # Parse AI response into structured plan
        plan = self._parse_ai_plan(user_goal, ai_plan)
        
        # Store as active plan
        self.active_plan = plan
        self.plan_history.append(plan)
        
        return plan
    
    def _parse_ai_plan(self, goal: str, ai_result: Dict[str, Any]) -> SessionPlan:
        """Parse AI result into SessionPlan"""
        
        # Extract phases from AI response
        phases = []
        
        # Try to extract structured phases
        recommendations = ai_result.get('recommendations', [])
        
        if recommendations:
            # Group recommendations into phases
            setup_actions = []
            main_actions = []
            finalize_actions = []
            
            for rec in recommendations:
                action = rec.get('action', '')
                priority = rec.get('priority', 'medium')
                
                if 'setup' in action.lower() or 'prepare' in action.lower():
                    setup_actions.append(action)
                elif 'finalize' in action.lower() or 'complete' in action.lower():
                    finalize_actions.append(action)
                else:
                    main_actions.append(action)
            
            # Create phases
            if setup_actions:
                phases.append(SessionPhase(
                    name="Setup & Preparation",
                    duration_minutes=15,
                    actions=setup_actions,
                    success_criteria=["Environment ready", "Tools loaded"]
                ))
            
            if main_actions:
                phases.append(SessionPhase(
                    name="Core Work",
                    duration_minutes=90,
                    actions=main_actions,
                    success_criteria=["Primary goal achieved"],
                    break_after=True
                ))
            
            if finalize_actions:
                phases.append(SessionPhase(
                    name="Finalization",
                    duration_minutes=15,
                    actions=finalize_actions,
                    success_criteria=["Work completed", "Changes saved"]
                ))
        
        # Default phases if none extracted
        if not phases:
            phases = [
                SessionPhase(
                    name="Planning",
                    duration_minutes=10,
                    actions=["Review goal", "Break down tasks"],
                    success_criteria=["Clear plan"]
                ),
                SessionPhase(
                    name="Execution",
                    duration_minutes=60,
                    actions=["Work on goal"],
                    success_criteria=["Progress made"],
                    break_after=True
                ),
                SessionPhase(
                    name="Review",
                    duration_minutes=10,
                    actions=["Review work", "Plan next steps"],
                    success_criteria=["Session complete"]
                )
            ]
        
        # Calculate total duration
        total_duration = sum(p.duration_minutes for p in phases)
        
        # Determine optimal start time
        context = self.ai_brain.context_analyzer.get_current_context()
        optimal_time = self._determine_optimal_time(context, total_duration)
        
        return SessionPlan(
            goal=goal,
            estimated_duration_minutes=total_duration,
            optimal_start_time=optimal_time,
            phases=phases,
            potential_blockers=ai_result.get('potential_blockers', []),
            success_criteria=ai_result.get('success_criteria', []),
            created_at=time.time()
        )
    
    def _determine_optimal_time(self, context, duration_minutes: int) -> str:
        """Determine optimal time to start based on context"""
        
        energy = context.cognitive.energy_level
        time_of_day = context.temporal.time_of_day
        
        if energy == "high" and time_of_day in ["morning", "afternoon"]:
            return "now"
        elif energy == "medium":
            return "now (but consider break first)"
        else:
            return "tomorrow morning"
    
    def get_current_phase(self) -> Optional[SessionPhase]:
        """Get current phase of active plan"""
        if not self.active_plan:
            return None
        
        # Calculate elapsed time
        elapsed = time.time() - self.active_plan.created_at
        elapsed_minutes = elapsed / 60
        
        # Find current phase
        cumulative = 0
        for phase in self.active_plan.phases:
            cumulative += phase.duration_minutes
            if elapsed_minutes < cumulative:
                return phase
        
        return None  # Session complete
    
    def get_progress(self) -> Dict[str, Any]:
        """Get progress on active plan"""
        if not self.active_plan:
            return {"status": "no_active_plan"}
        
        elapsed = time.time() - self.active_plan.created_at
        elapsed_minutes = elapsed / 60
        total_minutes = self.active_plan.estimated_duration_minutes
        
        progress_pct = min(100, (elapsed_minutes / total_minutes) * 100)
        
        current_phase = self.get_current_phase()
        
        return {
            "status": "in_progress" if current_phase else "complete",
            "progress_percent": progress_pct,
            "elapsed_minutes": int(elapsed_minutes),
            "remaining_minutes": max(0, total_minutes - int(elapsed_minutes)),
            "current_phase": current_phase.name if current_phase else "Complete",
            "goal": self.active_plan.goal
        }
    
    def should_take_break(self) -> bool:
        """Determine if user should take a break"""
        if not self.active_plan:
            return False
        
        current_phase = self.get_current_phase()
        if not current_phase:
            return False
        
        # Check if current phase suggests break
        if current_phase.break_after:
            # Check if phase is almost complete
            elapsed = time.time() - self.active_plan.created_at
            elapsed_minutes = elapsed / 60
            
            # Find phase start time
            phase_start = 0
            for phase in self.active_plan.phases:
                if phase.name == current_phase.name:
                    break
                phase_start += phase.duration_minutes
            
            phase_elapsed = elapsed_minutes - phase_start
            phase_progress = phase_elapsed / current_phase.duration_minutes
            
            # Suggest break if 80%+ through phase
            return phase_progress >= 0.8
        
        return False


class GoalOptimizer:
    """
    Optimizes approach to achieving goals
    
    Not just planning - OPTIMIZING for best results
    """
    
    def __init__(self, ai_brain: AIBrain):
        self.ai_brain = ai_brain
    
    def optimize_approach(self, goal: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize the approach to achieving a goal
        
        Considers constraints like time, energy, resources
        """
        
        context = self.ai_brain.context_analyzer.get_current_context()
        
        # Build optimization prompt
        situation = {
            "goal": goal,
            "constraints": constraints,
            "context": context.to_dict()
        }
        
        question = f"""
        How can the user optimally achieve this goal: {goal}
        
        Given constraints:
        {json.dumps(constraints, indent=2)}
        
        Consider:
        1. Most efficient approach
        2. Best timing based on energy/context
        3. Potential shortcuts or optimizations
        4. Risk mitigation strategies
        5. Success probability
        
        Provide specific, actionable optimization recommendations.
        """
        
        result = self.ai_brain.think(situation, question)
        
        return result
    
    def suggest_goal_breakdown(self, large_goal: str) -> List[str]:
        """Break down a large goal into smaller achievable goals"""
        
        situation = {"goal": large_goal}
        
        question = f"""
        Break down this large goal into smaller, achievable sub-goals: {large_goal}
        
        Each sub-goal should be:
        1. Specific and measurable
        2. Achievable in 1-3 hours
        3. Build toward the larger goal
        4. Have clear success criteria
        
        Provide 3-5 sub-goals in order.
        """
        
        result = self.ai_brain.think(situation, question)
        
        # Extract sub-goals from recommendations
        recommendations = result.get('recommendations', [])
        sub_goals = [rec.get('action', '') for rec in recommendations]
        
        return sub_goals if sub_goals else [large_goal]


class TacticalIntelligence:
    """
    Main tactical intelligence coordinator
    
    Strategic session planning and goal optimization
    """
    
    def __init__(self, ai_brain: AIBrain):
        self.ai_brain = ai_brain
        self.session_planner = SessionPlanner(ai_brain)
        self.goal_optimizer = GoalOptimizer(ai_brain)
    
    def plan_work_session(self, goal: str) -> SessionPlan:
        """Plan a complete work session"""
        return self.session_planner.create_session_plan(goal)
    
    def get_session_progress(self) -> Dict[str, Any]:
        """Get progress on current session"""
        return self.session_planner.get_progress()
    
    def optimize_goal(self, goal: str, constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Optimize approach to a goal"""
        if constraints is None:
            constraints = {}
        return self.goal_optimizer.optimize_approach(goal, constraints)
    
    def break_down_goal(self, large_goal: str) -> List[str]:
        """Break down a large goal"""
        return self.goal_optimizer.suggest_goal_breakdown(large_goal)
    
    def should_suggest_break(self) -> bool:
        """Check if should suggest a break"""
        return self.session_planner.should_take_break()


if __name__ == "__main__":
    # Test tactical intelligence
    from pathlib import Path
    import os
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set")
        exit(1)
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🎯 TACTICAL INTELLIGENCE TEST")
    print("=" * 60)
    print()
    
    # Initialize
    ai_brain = AIBrain(data_dir)
    tactical = TacticalIntelligence(ai_brain)
    
    # Test 1: Plan session
    print("Test 1: Planning work session...")
    print("Goal: Implement predictive engine for JarvisOS")
    print()
    
    plan = tactical.plan_work_session("Implement predictive engine for JarvisOS")
    
    print(f"Session Plan Created:")
    print(f"  Goal: {plan.goal}")
    print(f"  Duration: {plan.estimated_duration_minutes} minutes")
    print(f"  Optimal Start: {plan.optimal_start_time}")
    print(f"  Phases: {len(plan.phases)}")
    print()
    
    for i, phase in enumerate(plan.phases, 1):
        print(f"  Phase {i}: {phase.name} ({phase.duration_minutes} min)")
        for action in phase.actions[:2]:
            print(f"    - {action[:60]}...")
    print()
    
    # Test 2: Break down goal
    print("Test 2: Breaking down large goal...")
    print("Goal: Launch JarvisOS v1.0")
    print()
    
    sub_goals = tactical.break_down_goal("Launch JarvisOS v1.0")
    
    print(f"Sub-goals: {len(sub_goals)}")
    for i, goal in enumerate(sub_goals, 1):
        print(f"  {i}. {goal}")
    print()
    
    print("=" * 60)
    print("✅ TACTICAL INTELLIGENCE IS WORKING!")
    print("=" * 60)
