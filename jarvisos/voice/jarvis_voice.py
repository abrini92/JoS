"""
JarvisOS Voice Interface
Main voice interaction system with personality
"""

import threading
import time
from typing import Optional, Callable
from datetime import datetime

from .tts import TextToSpeech, get_jarvis_voice
from .stt import SpeechToText
from ..utils.logger import get_logger

logger = get_logger("jarvisos.voice")


class JarvisVoice:
    """Jarvis voice interface with personality"""
    
    def __init__(self, user_name: Optional[str] = None):
        """
        Initialize Jarvis voice
        
        Args:
            user_name: User's name for personalization
        """
        self.user_name = user_name or "there"
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        self.listening = False
        self.wake_word = "hey jarvis"
        
        # Get Jarvis voice
        self.voice = get_jarvis_voice(self.tts.engine, 'default')
        
        logger.info(f"JarvisVoice initialized for user: {self.user_name}")
    
    def speak(self, text: str, rate: int = 175):
        """
        Speak with Jarvis personality
        
        Args:
            text: Text to speak
            rate: Speech rate
        """
        logger.info(f"Jarvis speaking: {text[:50]}...")
        self.tts.speak(text, voice=self.voice, rate=rate)
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for user speech
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Transcribed text or None
        """
        return self.stt.listen(timeout=timeout)
    
    def greet(self):
        """Greet the user"""
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = f"Good morning, {self.user_name}."
        elif hour < 18:
            greeting = f"Good afternoon, {self.user_name}."
        else:
            greeting = f"Good evening, {self.user_name}."
        
        self.speak(greeting)
    
    def introduce(self):
        """Introduce Jarvis"""
        intro = f"""Hello, {self.user_name}. I am Jarvis.
        
I am not an ordinary operating system.

I am here to learn who you are, how you work, and what you need.

I will observe your behavior, analyze your patterns, and generate automations specifically for you.

Over time, I will evolve to become the perfect operating system for you, and only you.

Let's begin."""
        
        self.speak(intro, rate=165)
    
    def confirm(self, message: str = "Understood."):
        """Confirm action"""
        self.speak(message)
    
    def acknowledge(self):
        """Acknowledge user"""
        responses = [
            "Yes?",
            "I'm listening.",
            "How can I help?",
            "What do you need?"
        ]
        import random
        self.speak(random.choice(responses))
    
    def notify(self, message: str):
        """Notify user of something"""
        self.speak(message)
    
    def ask_question(self, question: str, timeout: int = 10) -> Optional[str]:
        """
        Ask user a question and get response
        
        Args:
            question: Question to ask
            timeout: Timeout for response
            
        Returns:
            User's response or None
        """
        self.speak(question)
        time.sleep(0.5)  # Brief pause
        return self.listen(timeout=timeout)
    
    def start_listening_loop(self, callback: Callable):
        """
        Start continuous listening for wake word
        
        Args:
            callback: Function to call when wake word detected
        """
        self.listening = True
        
        def listen_loop():
            logger.info("Starting wake word detection loop...")
            
            while self.listening:
                try:
                    detected = self.stt.listen_for_wake_word(
                        wake_word=self.wake_word,
                        callback=callback,
                        timeout=5
                    )
                    
                    if detected:
                        self.acknowledge()
                        
                except Exception as e:
                    logger.error(f"Error in listening loop: {e}")
                    time.sleep(1)
        
        # Start in background thread
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
        logger.info("Wake word detection started")
    
    def stop_listening(self):
        """Stop listening loop"""
        self.listening = False
        logger.info("Wake word detection stopped")
    
    def onboarding_conversation(self) -> dict:
        """
        Interactive onboarding conversation
        
        Returns:
            User profile data
        """
        profile = {}
        
        # Introduction
        self.introduce()
        time.sleep(1)
        
        # Question 1: Name
        self.speak("First, what's your name?")
        name = self.listen(timeout=10)
        if name:
            profile['name'] = name
            self.user_name = name
            self.speak(f"Nice to meet you, {name}.")
        
        time.sleep(0.5)
        
        # Question 2: Primary activity
        self.speak("What do you primarily do on your computer?")
        self.speak("For example: development, design, business, or something else?")
        activity = self.listen(timeout=10)
        if activity:
            profile['primary_activity'] = activity
            self.speak(f"{activity}. Got it.")
        
        time.sleep(0.5)
        
        # Question 3: Tools
        self.speak("What tools or applications do you use most?")
        tools = self.listen(timeout=10)
        if tools:
            profile['primary_tools'] = tools
            self.speak("Noted.")
        
        time.sleep(0.5)
        
        # Question 4: Work schedule
        self.speak("When do you typically work? Morning, afternoon, or evening?")
        schedule = self.listen(timeout=10)
        if schedule:
            profile['work_schedule'] = schedule
            self.speak("Understood.")
        
        time.sleep(0.5)
        
        # Question 5: Frustrations
        self.speak("What frustrates you most about your current workflow?")
        frustrations = self.listen(timeout=15)
        if frustrations:
            profile['frustrations'] = frustrations
            self.speak("I can help with that.")
        
        time.sleep(0.5)
        
        # Permission
        self.speak(f"One last thing, {self.user_name}.")
        self.speak("May I observe how you work for a few days?")
        self.speak("I promise all data stays local, and you control everything.")
        self.speak("Say yes or no.")
        
        permission = self.listen(timeout=10)
        if permission and 'yes' in permission.lower():
            profile['observation_permission'] = True
            self.speak("Thank you.")
            self.speak("I'll observe quietly for a few days.")
            self.speak("In three days, I'll return with personalized suggestions.")
            self.speak(f"Until then, work normally. I'm here if you need me.")
            self.speak(f"Just say: Hey Jarvis.")
        else:
            profile['observation_permission'] = False
            self.speak("I understand. You can enable observation anytime.")
        
        time.sleep(0.5)
        self.speak(f"Good luck, {self.user_name}.")
        
        return profile
    
    def daily_checkin(self):
        """Daily check-in with user"""
        hour = datetime.now().hour
        
        if hour < 12:
            self.speak(f"Good morning, {self.user_name}. Ready to start the day?")
        elif hour < 18:
            self.speak(f"Good afternoon, {self.user_name}. How's your day going?")
        else:
            self.speak(f"Good evening, {self.user_name}. Wrapping up for the day?")
    
    def suggest_break(self):
        """Suggest user take a break"""
        self.speak(f"{self.user_name}, you've been working for a while.")
        self.speak("Consider taking a short break. It helps productivity.")
    
    def celebrate_achievement(self, achievement: str):
        """Celebrate user achievement"""
        self.speak(f"Well done, {self.user_name}!")
        self.speak(achievement)


# Example usage
if __name__ == "__main__":
    jarvis = JarvisVoice(user_name="Marc")
    
    print("Testing Jarvis voice...")
    
    # Test greeting
    jarvis.greet()
    time.sleep(1)
    
    # Test introduction
    jarvis.introduce()
    time.sleep(1)
    
    # Test question
    response = jarvis.ask_question("How are you today?")
    if response:
        print(f"User said: {response}")
        jarvis.confirm("Great to hear!")
