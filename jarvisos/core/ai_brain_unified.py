#!/usr/bin/env python3
"""
JarvisOS - Unified AI Brain
Automatically chooses between Ollama (local) and Claude (API)

Priority:
1. Ollama (if available) - Free, private, fast
2. Claude API (fallback) - Powerful but requires API key
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Try importing both
try:
    from .ai_brain_ollama import OllamaAIBrain, get_ollama_brain
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False

try:
    from .ai_brain import AIBrain as ClaudeAIBrain
    CLAUDE_AVAILABLE = True
except:
    CLAUDE_AVAILABLE = False


@dataclass
class AICapabilities:
    """Available AI capabilities"""
    has_ollama: bool
    has_claude: bool
    active_brain: str  # "ollama", "claude", or "none"


class UnifiedAIBrain:
    """
    Unified AI Brain that automatically selects the best available option
    
    Strategy:
    - Prefer Ollama (local, free, privacy)
    - Fallback to Claude if Ollama unavailable
    - Graceful degradation if no AI available
    """
    
    def __init__(self):
        self.ollama_brain = None
        self.claude_brain = None
        self.active = None
        
        # Try Ollama first
        if OLLAMA_AVAILABLE:
            try:
                self.ollama_brain = get_ollama_brain()
                if self.ollama_brain and self.ollama_brain.available:
                    self.active = "ollama"
            except:
                self.ollama_brain = None
        
        # Try Claude as fallback
        if not self.active and CLAUDE_AVAILABLE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                try:
                    self.claude_brain = ClaudeAIBrain(api_key=api_key)
                    self.active = "claude"
                except:
                    self.claude_brain = None
        
        # No AI available
        if not self.active:
            self.active = "none"
    
    def get_capabilities(self) -> AICapabilities:
        """Get current AI capabilities"""
        return AICapabilities(
            has_ollama=self.ollama_brain is not None,
            has_claude=self.claude_brain is not None,
            active_brain=self.active
        )
    
    def is_available(self) -> bool:
        """Check if any AI is available"""
        return self.active != "none"
    
    def predict_next_action(self, context: Dict[str, Any]) -> Optional[str]:
        """Predict user's next action"""
        if self.active == "ollama" and self.ollama_brain:
            return self.ollama_brain.predict_next_action(context)
        elif self.active == "claude" and self.claude_brain:
            return self.claude_brain.predict(context)
        else:
            return None
    
    def generate_script(self, description: str, observations: list) -> Optional[str]:
        """Generate a script based on description"""
        if self.active == "ollama" and self.ollama_brain:
            return self.ollama_brain.generate_script(description, observations)
        elif self.active == "claude" and self.claude_brain:
            # Claude brain would need this method
            return None
        else:
            return None
    
    def plan_task(self, goal: str, context: Optional[Dict] = None) -> Optional[str]:
        """Create a strategic plan"""
        if self.active == "ollama" and self.ollama_brain:
            return self.ollama_brain.plan_task(goal, context)
        elif self.active == "claude" and self.claude_brain:
            return self.claude_brain.plan(goal, context or {})
        else:
            return None
    
    def analyze_session(self, session_data: Dict[str, Any]) -> Optional[str]:
        """Analyze work session"""
        if self.active == "ollama" and self.ollama_brain:
            return self.ollama_brain.analyze_work_session(session_data)
        elif self.active == "claude" and self.claude_brain:
            return self.claude_brain.analyze(session_data)
        else:
            return None
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate text from prompt (generic method)"""
        if self.active == "ollama" and self.ollama_brain:
            return self.ollama_brain.generate(prompt)
        elif self.active == "claude" and self.claude_brain:
            # Use Claude's message API
            try:
                message = self.claude_brain.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except:
                return None
        else:
            return None
    
    def get_status_message(self) -> str:
        """Get human-readable status"""
        if self.active == "ollama":
            model = self.ollama_brain.config.model if self.ollama_brain else "unknown"
            return f"✅ AI: Ollama ({model}) - Local & Free"
        elif self.active == "claude":
            return f"✅ AI: Claude Haiku - API"
        else:
            return "⚠️  AI: Not available (install Ollama or add Claude API key)"


# Singleton
_unified_brain: Optional[UnifiedAIBrain] = None

def get_ai_brain() -> UnifiedAIBrain:
    """Get the unified AI brain (singleton)"""
    global _unified_brain
    if _unified_brain is None:
        _unified_brain = UnifiedAIBrain()
    return _unified_brain

# Alias for compatibility
get_unified_brain = get_ai_brain

def get_ai_status() -> str:
    """Get AI status message"""
    brain = get_ai_brain()
    return brain.get_status_message()


# Convenience functions
def predict(context: Dict[str, Any]) -> Optional[str]:
    """Predict next action"""
    return get_ai_brain().predict_next_action(context)

def plan(goal: str, context: Optional[Dict] = None) -> Optional[str]:
    """Plan a task"""
    return get_ai_brain().plan_task(goal, context)

def generate_script(description: str, observations: list) -> Optional[str]:
    """Generate a script"""
    return get_ai_brain().generate_script(description, observations)


if __name__ == "__main__":
    # Test
    brain = get_ai_brain()
    caps = brain.get_capabilities()
    
    print("🤖 JarvisOS AI Brain Status")
    print("=" * 40)
    print(f"Ollama: {'✅' if caps.has_ollama else '❌'}")
    print(f"Claude: {'✅' if caps.has_claude else '❌'}")
    print(f"Active: {caps.active_brain}")
    print()
    print(brain.get_status_message())
