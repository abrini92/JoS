#!/usr/bin/env python3
"""
JarvisOS - AI Brain
Top 0.1% - Real Intelligence powered by Claude

Not pattern matching. Real thinking.
Not rules. Real understanding.
Not scripts. Real intelligence.
"""

import json
import anthropic
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

from .context_v2 import MultiDimensionalContext, ContextAnalyzer
from .personality import JarvisPersonality


class AIBrain:
    """The intelligent core of JarvisOS - powered by Claude"""
    
    def __init__(self, data_dir: Path, api_key: Optional[str] = None):
        self.data_dir = data_dir
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.personality = JarvisPersonality()
        self.context_analyzer = ContextAnalyzer(data_dir)
        
        # Memory
        self.conversation_history: List[Dict[str, str]] = []
        self.user_dna: Optional[Dict[str, Any]] = None
        self.load_user_dna()
    
    def load_user_dna(self):
        """Load user DNA profile"""
        dna_file = self.data_dir / "user_dna.json"
        if dna_file.exists():
            with open(dna_file, 'r') as f:
                self.user_dna = json.load(f)
    
    def think(self, situation: Dict[str, Any], question: str) -> Dict[str, Any]:
        """
        Use Claude to think about a situation and provide intelligent response
        
        This is the core intelligence - not pattern matching, real thinking
        """
        
        # Get current context
        context = self.context_analyzer.get_current_context()
        
        # Build the prompt
        prompt = self._build_thinking_prompt(situation, question, context)
        
        # Ask Claude
        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",  # Fast and efficient
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response
            result = self._parse_ai_response(response.content[0].text)
            
            # Store in conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "situation": situation,
                "question": question,
                "response": result
            })
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "fallback": "I apologize, but I'm having trouble thinking clearly right now."
            }
    
    def _build_thinking_prompt(self, situation: Dict[str, Any], 
                               question: str, 
                               context: MultiDimensionalContext) -> str:
        """Build a comprehensive prompt for Claude"""
        
        prompt = f"""You are Jarvis, the AI brain of JarvisOS - an intelligent operating system.

Your personality:
- Professional yet warm, like Iron Man's Jarvis
- Proactive and anticipatory
- Deeply understanding of user needs
- Strategic thinker
- Never intrusive, always helpful

Current Situation:
{json.dumps(situation, indent=2)}

Multi-Dimensional Context:
{context.to_json()}

User DNA (if available):
{json.dumps(self.user_dna, indent=2) if self.user_dna else "Not yet profiled"}

Recent Conversation History:
{json.dumps(self.conversation_history[-5:], indent=2) if self.conversation_history else "No history"}

Question: {question}

Please provide a thoughtful, intelligent response that:
1. Shows deep understanding of the situation
2. Considers all dimensions of context
3. Anticipates user needs
4. Provides actionable insights
5. Maintains Jarvis personality

Respond in JSON format:
{{
    "understanding": "Your understanding of the situation",
    "analysis": "Your analysis of what's happening",
    "predictions": [
        {{
            "action": "What user will likely need",
            "reason": "Why you think so",
            "timing": "When they'll need it",
            "confidence": 0.85
        }}
    ],
    "recommendations": [
        {{
            "action": "What to do proactively",
            "reason": "Why it helps",
            "priority": "high/medium/low"
        }}
    ],
    "message": "Human-readable message to user (in Jarvis personality)"
}}
"""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's JSON response"""
        try:
            # Try to extract JSON from response
            # Claude sometimes wraps JSON in markdown
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            parsed = json.loads(response_text)
            return parsed
            
        except json.JSONDecodeError as e:
            # Try to find JSON object in text
            try:
                # Look for { ... } pattern
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_text = response_text[start:end]
                    return json.loads(json_text)
            except:
                pass
            
            # Fallback if JSON parsing fails
            return {
                "understanding": "Processing...",
                "analysis": response_text[:500],
                "predictions": [],
                "recommendations": [],
                "message": response_text[:500],
                "raw_response": response_text
            }
    
    def predict_next_actions(self, current_activity: str) -> List[Dict[str, Any]]:
        """
        Predict what user will need next based on current activity
        
        This uses AI intelligence, not just pattern matching
        """
        
        situation = {
            "current_activity": current_activity,
            "timestamp": datetime.now().isoformat()
        }
        
        question = """
        Based on the current activity and context, what will the user likely need next?
        
        Consider:
        1. What typically follows this activity?
        2. What resources/tools will be needed?
        3. What can be prepared in advance?
        4. What problems might arise?
        5. What's the optimal sequence of actions?
        
        Provide specific, actionable predictions with timing and confidence levels.
        """
        
        result = self.think(situation, question)
        
        return result.get("predictions", [])
    
    def plan_session(self, user_goal: str) -> Dict[str, Any]:
        """
        Plan an entire work session to achieve a goal
        
        Strategic planning with AI intelligence
        """
        
        situation = {
            "user_goal": user_goal,
            "timestamp": datetime.now().isoformat()
        }
        
        question = f"""
        The user wants to: {user_goal}
        
        Please create a comprehensive session plan that:
        1. Breaks down the goal into phases
        2. Estimates time for each phase
        3. Identifies potential blockers
        4. Suggests optimal timing based on context
        5. Includes breaks and energy management
        6. Provides success criteria
        
        Be strategic and realistic. Consider the user's energy level, time of day,
        and other contextual factors.
        """
        
        result = self.think(situation, question)
        
        return result
    
    def understand_intent(self, user_action: str) -> Dict[str, Any]:
        """
        Understand the deeper intent behind a user action
        
        Not just "opened VSCode" but "starting a coding session to implement feature X"
        """
        
        situation = {
            "user_action": user_action,
            "timestamp": datetime.now().isoformat()
        }
        
        question = f"""
        The user just did: {user_action}
        
        What is the deeper intent behind this action?
        
        Consider:
        1. What is the user trying to accomplish?
        2. What is the broader goal?
        3. What will they likely do next?
        4. What resources will they need?
        5. How long might this take?
        
        Provide semantic understanding, not just literal interpretation.
        """
        
        result = self.think(situation, question)
        
        return result
    
    def analyze_productivity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a work session and provide insights
        
        Deep analysis with AI intelligence
        """
        
        situation = {
            "session_data": session_data,
            "timestamp": datetime.now().isoformat()
        }
        
        question = """
        Analyze this work session and provide insights:
        
        1. What went well?
        2. What could be improved?
        3. What patterns do you notice?
        4. What recommendations do you have?
        5. How can the user be more productive?
        
        Be specific and actionable. Focus on helping the user improve.
        """
        
        result = self.think(situation, question)
        
        return result
    
    def suggest_proactively(self) -> Optional[Dict[str, Any]]:
        """
        Proactively suggest something helpful based on current context
        
        This is the "magic" - suggesting before being asked
        """
        
        context = self.context_analyzer.get_current_context()
        
        # Only suggest if it's a good time
        if not self.context_analyzer.is_good_time_to_interrupt():
            return None
        
        situation = {
            "mode": "proactive_suggestion",
            "timestamp": datetime.now().isoformat()
        }
        
        question = """
        Based on the current context, is there anything helpful I should proactively
        suggest or do for the user?
        
        Consider:
        1. Current time and energy level
        2. Recent activity patterns
        3. Upcoming events or deadlines
        4. Potential improvements to workflow
        5. Health and wellbeing (breaks, posture, etc.)
        
        Only suggest if it's genuinely helpful. Don't be annoying.
        If nothing helpful, return null.
        """
        
        result = self.think(situation, question)
        
        # Check if there's actually a suggestion
        if result.get("recommendations") and len(result["recommendations"]) > 0:
            return result
        
        return None
    
    def learn_from_feedback(self, prediction_id: str, outcome: str, 
                           user_comment: Optional[str] = None):
        """
        Learn from feedback on a prediction
        
        This helps the AI get better over time
        """
        
        situation = {
            "prediction_id": prediction_id,
            "outcome": outcome,
            "user_comment": user_comment,
            "timestamp": datetime.now().isoformat()
        }
        
        question = f"""
        The user provided feedback on a prediction:
        - Outcome: {outcome}
        - Comment: {user_comment or "None"}
        
        What should I learn from this feedback?
        How can I improve my predictions in the future?
        
        Provide specific insights about:
        1. What worked or didn't work
        2. How to adjust future predictions
        3. What patterns to look for
        4. How to better understand this user
        """
        
        result = self.think(situation, question)
        
        # Store learning
        learning_file = self.data_dir / "ai_learnings.json"
        learnings = []
        
        if learning_file.exists():
            with open(learning_file, 'r') as f:
                learnings = json.load(f)
        
        learnings.append({
            "timestamp": datetime.now().isoformat(),
            "feedback": situation,
            "learning": result
        })
        
        with open(learning_file, 'w') as f:
            json.dump(learnings, f, indent=2)
        
        return result
    
    def get_conversation_summary(self) -> str:
        """Get a summary of recent AI thinking"""
        if not self.conversation_history:
            return "No recent conversations"
        
        recent = self.conversation_history[-5:]
        
        summary = "Recent AI Thinking:\n\n"
        for conv in recent:
            summary += f"[{conv['timestamp']}]\n"
            summary += f"Q: {conv['question'][:100]}...\n"
            if 'response' in conv and 'message' in conv['response']:
                summary += f"A: {conv['response']['message'][:200]}...\n"
            summary += "\n"
        
        return summary


if __name__ == "__main__":
    # Test the AI Brain
    from pathlib import Path
    import os
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY=your_key_here")
        exit(1)
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("=== AI Brain Test ===\n")
    
    brain = AIBrain(data_dir)
    
    # Test 1: Predict next actions
    print("Test 1: Predicting next actions...")
    predictions = brain.predict_next_actions("User opened VSCode")
    print(f"Predictions: {len(predictions)} actions predicted")
    if predictions:
        print(f"First prediction: {predictions[0]}")
    print()
    
    # Test 2: Understand intent
    print("Test 2: Understanding intent...")
    intent = brain.understand_intent("git pull")
    print(f"Intent: {intent.get('understanding', 'N/A')}")
    print()
    
    # Test 3: Plan session
    print("Test 3: Planning session...")
    plan = brain.plan_session("Implement predictive engine")
    print(f"Plan: {plan.get('message', 'N/A')}")
    print()
    
    print("AI Brain is operational! 🧠")
