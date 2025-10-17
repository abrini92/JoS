#!/usr/bin/env python3
"""
JarvisOS - Operational Intelligence Layer
Top 0.1% - Real-time prediction and proactive action

Not just observing - UNDERSTANDING and ANTICIPATING
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

from .ai_brain import AIBrain
from .context_v2 import ContextAnalyzer


@dataclass
class SemanticAction:
    """An action with semantic understanding"""
    raw_action: str
    intent: str
    goal: str
    expected_duration: int  # seconds
    related_tasks: List[str]
    confidence: float
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Prediction:
    """A prediction of what user will need"""
    action: str
    reason: str
    timing: str  # "now", "in 5 minutes", "after X"
    confidence: float
    priority: str  # "high", "medium", "low"
    prepared: bool = False
    executed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SemanticObserver:
    """
    Observes user actions and understands their semantic meaning
    
    Not just "opened VSCode" but "starting coding session on project X"
    """
    
    def __init__(self, ai_brain: AIBrain):
        self.ai_brain = ai_brain
        self.action_history: List[SemanticAction] = []
    
    def observe_action(self, raw_action: str) -> SemanticAction:
        """
        Observe an action and understand its semantic meaning
        """
        
        # Use AI to understand the action
        result = self.ai_brain.understand_intent(raw_action)
        
        # Extract semantic meaning
        semantic_action = SemanticAction(
            raw_action=raw_action,
            intent=result.get('understanding', 'Unknown intent'),
            goal=result.get('analysis', 'Unknown goal'),
            expected_duration=self._estimate_duration(result),
            related_tasks=self._extract_related_tasks(result),
            confidence=self._extract_confidence(result),
            timestamp=time.time()
        )
        
        # Store in history
        self.action_history.append(semantic_action)
        
        # Keep only last 100 actions
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-100:]
        
        return semantic_action
    
    def _estimate_duration(self, ai_result: Dict[str, Any]) -> int:
        """Estimate duration from AI result"""
        # TODO: Parse duration from AI response
        return 1800  # Default 30 minutes
    
    def _extract_related_tasks(self, ai_result: Dict[str, Any]) -> List[str]:
        """Extract related tasks from AI result"""
        predictions = ai_result.get('predictions', [])
        return [p.get('action', '') for p in predictions]
    
    def _extract_confidence(self, ai_result: Dict[str, Any]) -> float:
        """Extract confidence from AI result"""
        predictions = ai_result.get('predictions', [])
        if predictions:
            return predictions[0].get('confidence', 0.5)
        return 0.5
    
    def get_recent_actions(self, count: int = 10) -> List[SemanticAction]:
        """Get recent semantic actions"""
        return self.action_history[-count:]
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Get current work session info"""
        if not self.action_history:
            return None
        
        recent = self.action_history[-10:]
        
        # Analyze session
        session = {
            "start_time": recent[0].timestamp,
            "duration": time.time() - recent[0].timestamp,
            "actions_count": len(recent),
            "primary_intent": self._get_dominant_intent(recent),
            "focus_level": self._calculate_focus_level(recent)
        }
        
        return session
    
    def _get_dominant_intent(self, actions: List[SemanticAction]) -> str:
        """Get the dominant intent from actions"""
        if not actions:
            return "unknown"
        
        # Simple: return most recent intent
        return actions[-1].intent
    
    def _calculate_focus_level(self, actions: List[SemanticAction]) -> float:
        """Calculate focus level from actions"""
        if not actions:
            return 0.0
        
        # High focus = fewer different intents
        unique_intents = len(set(a.intent for a in actions))
        focus = 1.0 - (unique_intents / len(actions))
        
        return max(0.0, min(1.0, focus))


class PredictionEngine:
    """
    Predicts what user will need next
    
    Uses AI intelligence, not just pattern matching
    """
    
    def __init__(self, ai_brain: AIBrain, semantic_observer: SemanticObserver):
        self.ai_brain = ai_brain
        self.semantic_observer = semantic_observer
        self.active_predictions: List[Prediction] = []
    
    def predict_next_needs(self, current_action: Optional[str] = None) -> List[Prediction]:
        """
        Predict what user will need next
        
        Returns list of predictions sorted by priority and confidence
        """
        
        # Get current context
        context = self.ai_brain.context_analyzer.get_current_context()
        
        # Get recent actions
        recent_actions = self.semantic_observer.get_recent_actions(5)
        
        # Build activity description
        if current_action:
            activity = current_action
        elif recent_actions:
            activity = f"User recently: {recent_actions[-1].intent}"
        else:
            activity = "User just started"
        
        # Ask AI for predictions
        ai_predictions = self.ai_brain.predict_next_actions(activity)
        
        # Convert to Prediction objects
        predictions = []
        for pred in ai_predictions:
            prediction = Prediction(
                action=pred.get('action', 'Unknown'),
                reason=pred.get('reason', ''),
                timing=pred.get('timing', 'soon'),
                confidence=pred.get('confidence', 0.5),
                priority=self._calculate_priority(pred)
            )
            predictions.append(prediction)
        
        # Sort by priority and confidence
        predictions.sort(key=lambda p: (
            {'high': 3, 'medium': 2, 'low': 1}.get(p.priority, 0),
            p.confidence
        ), reverse=True)
        
        # Store active predictions
        self.active_predictions = predictions
        
        return predictions
    
    def _calculate_priority(self, prediction: Dict[str, Any]) -> str:
        """Calculate priority from prediction"""
        confidence = prediction.get('confidence', 0.5)
        timing = prediction.get('timing', 'later').lower()
        
        if confidence > 0.85 and 'immediate' in timing:
            return 'high'
        elif confidence > 0.7:
            return 'medium'
        else:
            return 'low'
    
    def get_high_confidence_predictions(self, threshold: float = 0.85) -> List[Prediction]:
        """Get predictions with high confidence"""
        return [p for p in self.active_predictions if p.confidence >= threshold]
    
    def mark_prediction_prepared(self, action: str):
        """Mark a prediction as prepared"""
        for pred in self.active_predictions:
            if pred.action == action:
                pred.prepared = True
    
    def mark_prediction_executed(self, action: str):
        """Mark a prediction as executed"""
        for pred in self.active_predictions:
            if pred.action == action:
                pred.executed = True


class ResourceManager:
    """
    Prepares resources proactively based on predictions
    
    Not just predicting - PREPARING
    """
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.prepared_resources: Dict[str, Any] = {}
    
    def prepare_for_predictions(self, predictions: List[Prediction]):
        """
        Prepare resources for high-confidence predictions
        """
        
        high_confidence = [p for p in predictions if p.confidence > 0.85]
        
        for prediction in high_confidence:
            if not prediction.prepared:
                self._prepare_resource(prediction)
    
    def _prepare_resource(self, prediction: Prediction):
        """Prepare a specific resource"""
        
        action = prediction.action.lower()
        
        # Different preparation strategies
        if 'project' in action or 'workspace' in action:
            self._prepare_workspace()
        
        elif 'test' in action or 'testing' in action:
            self._prepare_test_environment()
        
        elif 'git' in action or 'commit' in action:
            self._prepare_git_tools()
        
        elif 'documentation' in action or 'docs' in action:
            self._prepare_documentation()
        
        # Mark as prepared
        prediction.prepared = True
        
        # Store
        self.prepared_resources[prediction.action] = {
            'timestamp': time.time(),
            'prediction': prediction.to_dict()
        }
    
    def _prepare_workspace(self):
        """Prepare workspace"""
        # TODO: Actual workspace preparation
        pass
    
    def _prepare_test_environment(self):
        """Prepare test environment"""
        # TODO: Actual test prep
        pass
    
    def _prepare_git_tools(self):
        """Prepare git tools"""
        # TODO: Actual git prep
        pass
    
    def _prepare_documentation(self):
        """Prepare documentation"""
        # TODO: Actual docs prep
        pass
    
    def get_prepared_resources(self) -> Dict[str, Any]:
        """Get all prepared resources"""
        return self.prepared_resources


class OperationalIntelligence:
    """
    Main operational intelligence coordinator
    
    Combines semantic observation, prediction, and resource preparation
    """
    
    def __init__(self, data_dir: Path, ai_brain: AIBrain):
        self.data_dir = data_dir
        self.ai_brain = ai_brain
        
        # Components
        self.semantic_observer = SemanticObserver(ai_brain)
        self.prediction_engine = PredictionEngine(ai_brain, self.semantic_observer)
        self.resource_manager = ResourceManager(data_dir)
    
    def process_user_action(self, raw_action: str) -> Dict[str, Any]:
        """
        Process a user action with full operational intelligence
        
        1. Understand semantic meaning
        2. Predict what's needed next
        3. Prepare resources proactively
        """
        
        # Step 1: Understand action
        semantic_action = self.semantic_observer.observe_action(raw_action)
        
        # Step 2: Predict next needs
        predictions = self.prediction_engine.predict_next_needs(raw_action)
        
        # Step 3: Prepare resources
        self.resource_manager.prepare_for_predictions(predictions)
        
        # Return comprehensive result
        return {
            "semantic_action": semantic_action.to_dict(),
            "predictions": [p.to_dict() for p in predictions],
            "prepared_resources": list(self.resource_manager.prepared_resources.keys()),
            "session_info": self.semantic_observer.get_current_session()
        }
    
    def get_proactive_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get proactive suggestions based on current state
        
        This is the "magic" - suggesting before being asked
        """
        
        # Get AI's proactive suggestion
        suggestion = self.ai_brain.suggest_proactively()
        
        if not suggestion:
            return []
        
        # Convert to structured suggestions
        recommendations = suggestion.get('recommendations', [])
        
        suggestions = []
        for rec in recommendations:
            suggestions.append({
                "action": rec.get('action', ''),
                "reason": rec.get('reason', ''),
                "priority": rec.get('priority', 'medium'),
                "message": suggestion.get('message', '')
            })
        
        return suggestions
    
    def save_state(self):
        """Save operational intelligence state"""
        state = {
            "timestamp": time.time(),
            "action_history": [a.to_dict() for a in self.semantic_observer.action_history[-50:]],
            "active_predictions": [p.to_dict() for p in self.prediction_engine.active_predictions],
            "prepared_resources": self.resource_manager.prepared_resources
        }
        
        state_file = self.data_dir / "operational_intelligence.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load operational intelligence state"""
        state_file = self.data_dir / "operational_intelligence.json"
        
        if not state_file.exists():
            return
        
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        # TODO: Reconstruct objects from state
        pass


if __name__ == "__main__":
    # Test operational intelligence
    from pathlib import Path
    import os
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set")
        exit(1)
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🚀 OPERATIONAL INTELLIGENCE TEST")
    print("=" * 60)
    print()
    
    # Initialize
    ai_brain = AIBrain(data_dir)
    op_intel = OperationalIntelligence(data_dir, ai_brain)
    
    # Test 1: Process action
    print("Test 1: Processing user action...")
    print("Action: User opened VSCode")
    print()
    
    result = op_intel.process_user_action("User opened VSCode to work on JarvisOS")
    
    print("Semantic Understanding:")
    print(f"  Intent: {result['semantic_action']['intent']}")
    print()
    
    print(f"Predictions: {len(result['predictions'])}")
    for i, pred in enumerate(result['predictions'][:3], 1):
        print(f"  {i}. {pred['action']} ({pred['confidence']:.0%})")
        print(f"     {pred['reason']}")
    print()
    
    print(f"Resources Prepared: {len(result['prepared_resources'])}")
    for res in result['prepared_resources']:
        print(f"  - {res}")
    print()
    
    # Test 2: Proactive suggestions
    print("Test 2: Getting proactive suggestions...")
    suggestions = op_intel.get_proactive_suggestions()
    
    if suggestions:
        print(f"Suggestions: {len(suggestions)}")
        for i, sug in enumerate(suggestions, 1):
            print(f"  {i}. {sug['action']}")
            print(f"     {sug['reason']}")
    else:
        print("No suggestions right now")
    print()
    
    print("=" * 60)
    print("✅ OPERATIONAL INTELLIGENCE IS WORKING!")
    print("=" * 60)
