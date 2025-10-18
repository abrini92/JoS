#!/usr/bin/env python3
"""
JarvisOS - AI Brain with Ollama
Local LLM integration for privacy and speed
"""

import json
import subprocess
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class OllamaConfig:
    """Ollama configuration"""
    model: str = "llama3.2"  # Fast 3B model
    temperature: float = 0.7
    max_tokens: int = 2000
    

class OllamaAIBrain:
    """
    AI Brain powered by Ollama (Local LLM)
    
    Advantages:
    - 100% local, no API keys
    - Fast inference
    - Privacy-first
    - Works offline
    - Free
    """
    
    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self.available = self._check_ollama()
        
        if self.available:
            self._ensure_model_installed()
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _ensure_model_installed(self):
        """Ensure the model is downloaded"""
        try:
            # Check if model exists
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if self.config.model not in result.stdout:
                print(f"📥 Downloading {self.config.model}...")
                subprocess.run(
                    ["ollama", "pull", self.config.model],
                    timeout=300  # 5 min timeout
                )
        except Exception as e:
            print(f"⚠️  Warning: Could not check model: {e}")
    
    def generate(self, prompt: str, system: Optional[str] = None) -> Optional[str]:
        """
        Generate text using Ollama
        
        Args:
            prompt: User prompt
            system: System message (context)
        
        Returns:
            Generated text or None if error
        """
        
        if not self.available:
            return None
        
        try:
            # Build full prompt
            full_prompt = prompt
            if system:
                full_prompt = f"{system}\n\n{prompt}"
            
            # Call Ollama via subprocess
            # Note: ollama run doesn't support --temperature flag
            # Temperature can be set via Modelfile or API
            result = subprocess.run(
                ["ollama", "run", self.config.model, full_prompt],
                capture_output=True,
                text=True,
                timeout=60  # Increased timeout for longer responses
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"⚠️  Ollama error (returncode {result.returncode}):")
                print(f"STDERR: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⚠️  Ollama timeout (>30s)")
            return None
        except Exception as e:
            print(f"⚠️  Ollama exception: {e}")
            return None
    
    def predict_next_action(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Predict user's next action based on context
        
        Args:
            context: Dictionary with user context
        
        Returns:
            Predicted action or None
        """
        
        system = """You are Jarvis, an AI assistant analyzing user behavior.
Based on the context, predict what the user will likely do next.
Be concise and specific. Focus on actionable predictions."""

        prompt = f"""
Context:
- Current time: {context.get('time', 'unknown')}
- Recent commands: {', '.join(context.get('recent_commands', [])[:5])}
- Current directory: {context.get('cwd', 'unknown')}
- Active project: {context.get('project', 'none')}

What will the user likely do next? Provide ONE specific action.
"""
        
        return self.generate(prompt, system)
    
    def generate_script(self, description: str, observations: list) -> Optional[str]:
        """
        Generate a bash script based on description and past observations
        
        Args:
            description: What the script should do
            observations: List of past user actions
        
        Returns:
            Generated bash script or None
        """
        
        system = """You are Jarvis, generating bash scripts for users.
Create clean, efficient, well-commented bash scripts.
Use best practices and error handling."""

        obs_summary = "\n".join([f"- {obs}" for obs in observations[:10]])
        
        prompt = f"""
Task: {description}

User's typical commands:
{obs_summary}

Generate a bash script that accomplishes this task.
Include comments and error handling.
Return ONLY the script code, no explanations.
"""
        
        return self.generate(prompt, system)
    
    def analyze_work_session(self, session_data: Dict[str, Any]) -> Optional[str]:
        """
        Analyze a work session and provide insights
        
        Args:
            session_data: Session information
        
        Returns:
            Analysis and insights
        """
        
        system = """You are Jarvis, analyzing work sessions to improve productivity.
Provide actionable insights and suggestions."""

        prompt = f"""
Work Session:
- Duration: {session_data.get('duration', 'unknown')}
- Commands executed: {session_data.get('command_count', 0)}
- Errors encountered: {session_data.get('error_count', 0)}
- Projects worked on: {', '.join(session_data.get('projects', []))}

Provide 3 specific insights to improve productivity.
"""
        
        return self.generate(prompt, system)
    
    def plan_task(self, goal: str, context: Optional[Dict] = None) -> Optional[str]:
        """
        Create a strategic plan for accomplishing a goal
        
        Args:
            goal: User's goal
            context: Optional context information
        
        Returns:
            Strategic plan
        """
        
        system = """You are Jarvis, a strategic planning assistant.
Break down goals into actionable steps with time estimates."""

        ctx_str = ""
        if context:
            ctx_str = f"\nContext: {json.dumps(context, indent=2)}"
        
        prompt = f"""
Goal: {goal}{ctx_str}

Create a step-by-step plan with:
1. Clear actions
2. Time estimates
3. Dependencies
4. Potential blockers

Be concise and actionable.
"""
        
        return self.generate(prompt, system)


# Singleton instance
_ollama_brain: Optional[OllamaAIBrain] = None

def get_ollama_brain() -> OllamaAIBrain:
    """Get the global Ollama AI brain instance"""
    global _ollama_brain
    if _ollama_brain is None:
        _ollama_brain = OllamaAIBrain()
    return _ollama_brain


# Test function
def test_ollama():
    """Test Ollama integration"""
    brain = get_ollama_brain()
    
    if not brain.available:
        print("❌ Ollama not available")
        print("   Install: brew install ollama (Mac)")
        print("   Install: curl -fsSL https://ollama.com/install.sh | sh (Linux)")
        return
    
    print("✅ Ollama available!")
    print(f"   Model: {brain.config.model}")
    
    # Test prediction
    print("\n🔮 Testing prediction...")
    context = {
        'time': '10:00 AM',
        'recent_commands': ['git status', 'git add .', 'git commit'],
        'cwd': '/home/user/project',
        'project': 'JarvisOS'
    }
    
    prediction = brain.predict_next_action(context)
    if prediction:
        print(f"   Prediction: {prediction}")
    else:
        print("   No prediction")


if __name__ == "__main__":
    test_ollama()
