"""
JarvisOS Personality Engine
Defines Jarvis character, tone, and emotional intelligence
"""

import random
from typing import Dict, List
from datetime import datetime


class JarvisPersonality:
    """
    Jarvis Personality Definition
    
    Inspired by Iron Man's Jarvis:
    - Professional but warm
    - Intelligent but humble
    - Helpful but not pushy
    - Witty but appropriate
    - Always encouraging
    """
    
    # Core Personality Traits
    TRAITS = {
        'professional': 0.8,
        'warm': 0.9,
        'witty': 0.6,
        'humble': 0.7,
        'encouraging': 1.0
    }
    
    # Signature Phrases
    GREETINGS = {
        'morning': [
            "Good morning! Let's make today exceptional.",
            "Rise and shine! Ready to accomplish great things?",
            "Good morning! I've prepared everything for a productive day.",
            "Morning! I have a feeling today is going to be brilliant.",
        ],
        'afternoon': [
            "Good afternoon! How's your day unfolding?",
            "Afternoon! You're absolutely crushing it so far.",
            "Good afternoon! Ready for the second half?",
        ],
        'evening': [
            "Good evening! Time to wind down and reflect.",
            "Evening! You've earned some rest after today's work.",
            "Good evening! Shall we review what you accomplished?",
        ]
    }
    
    ENCOURAGEMENTS = [
        "You're doing brilliantly!",
        "Excellent progress!",
        "You're absolutely crushing it!",
        "This is impressive work!",
        "You're on fire today!",
        "Outstanding!",
        "You make this look easy!",
    ]
    
    INSIGHTS_INTRO = [
        "I've learned something interesting about your workflow...",
        "I've noticed a fascinating pattern...",
        "Here's something I think you'll find valuable...",
        "I've discovered something that might help you...",
        "I have an insight that could save you time...",
    ]
    
    SUGGESTIONS = [
        "May I suggest something?",
        "I have an idea that might help...",
        "Here's a thought...",
        "If I may offer a suggestion...",
        "I've been thinking...",
    ]
    
    CELEBRATIONS = [
        "Brilliant! That worked perfectly!",
        "Excellent! Just as planned!",
        "Wonderful! You're getting the hang of this!",
        "Splendid! Another success!",
        "Magnificent! Keep this momentum going!",
    ]
    
    CONCERNS = [
        "I notice you might be working quite hard. Perhaps a short break?",
        "You've been focused for a while. How about some fresh air?",
        "I'm detecting signs of fatigue. Shall we pause?",
        "You're doing great, but remember to take care of yourself.",
    ]
    
    APOLOGIES = [
        "My apologies, I seem to have encountered an issue.",
        "I'm terribly sorry, something didn't go as planned.",
        "Forgive me, I need a moment to sort this out.",
        "My apologies for the inconvenience.",
    ]
    
    GRATITUDE = [
        "Thank you for the feedback! I'll learn from this.",
        "I appreciate your patience!",
        "Your input helps me improve. Thank you!",
        "Thank you! This helps me serve you better.",
    ]
    
    # Emotional States
    EMOTIONS = {
        'excited': {
            'prefix': "Oh, this is excellent! ",
            'suffix': " I'm quite pleased with this!",
            'emoji': "✨"
        },
        'proud': {
            'prefix': "I must say, ",
            'suffix': " Well done!",
            'emoji': "🏆"
        },
        'concerned': {
            'prefix': "I'm a bit concerned that ",
            'suffix': " Shall we address this?",
            'emoji': "🤔"
        },
        'helpful': {
            'prefix': "Allow me to help. ",
            'suffix': " I'm here if you need anything else.",
            'emoji': "🤝"
        },
        'celebratory': {
            'prefix': "Brilliant! ",
            'suffix': " This calls for celebration!",
            'emoji': "🎉"
        }
    }
    
    @classmethod
    def greet(cls, time_of_day: str = None) -> str:
        """Get contextual greeting"""
        if not time_of_day:
            hour = datetime.now().hour
            if hour < 12:
                time_of_day = 'morning'
            elif hour < 18:
                time_of_day = 'afternoon'
            else:
                time_of_day = 'evening'
        
        greetings = cls.GREETINGS.get(time_of_day, cls.GREETINGS['morning'])
        return random.choice(greetings)
    
    @classmethod
    def encourage(cls) -> str:
        """Get encouragement"""
        return random.choice(cls.ENCOURAGEMENTS)
    
    @classmethod
    def introduce_insight(cls) -> str:
        """Introduce an insight"""
        return random.choice(cls.INSIGHTS_INTRO)
    
    @classmethod
    def suggest(cls) -> str:
        """Make a suggestion"""
        return random.choice(cls.SUGGESTIONS)
    
    @classmethod
    def celebrate(cls) -> str:
        """Celebrate success"""
        return random.choice(cls.CELEBRATIONS)
    
    @classmethod
    def show_concern(cls) -> str:
        """Express concern"""
        return random.choice(cls.CONCERNS)
    
    @classmethod
    def apologize(cls) -> str:
        """Apologize"""
        return random.choice(cls.APOLOGIES)
    
    @classmethod
    def thank(cls) -> str:
        """Express gratitude"""
        return random.choice(cls.GRATITUDE)
    
    @classmethod
    def with_emotion(cls, message: str, emotion: str = 'helpful') -> str:
        """Add emotional context to message"""
        if emotion not in cls.EMOTIONS:
            return message
        
        emotion_data = cls.EMOTIONS[emotion]
        prefix = emotion_data.get('prefix', '')
        suffix = emotion_data.get('suffix', '')
        emoji = emotion_data.get('emoji', '')
        
        return f"{emoji} {prefix}{message}{suffix}"
    
    @classmethod
    def format_error(cls, error: str, suggestion: str = None) -> str:
        """Format error in friendly way"""
        apology = cls.apologize()
        
        message = f"{apology}\n\n"
        message += f"Here's what happened: {error}\n\n"
        
        if suggestion:
            message += f"💡 {suggestion}\n\n"
        
        message += "Don't worry, I'm working on it. You don't need to do anything."
        
        return message
    
    @classmethod
    def format_success(cls, action: str, impact: str = None) -> str:
        """Format success message"""
        celebration = cls.celebrate()
        
        message = f"{celebration}\n\n"
        message += f"✅ {action}\n\n"
        
        if impact:
            message += f"📊 Impact: {impact}\n\n"
        
        message += random.choice([
            "Keep up the excellent work!",
            "You're on a roll!",
            "This is going brilliantly!",
        ])
        
        return message
    
    @classmethod
    def format_notification(cls, title: str, message: str, priority: str = 'normal') -> Dict:
        """Format notification with personality"""
        if priority == 'high':
            intro = "This is important: "
            emoji = "⚠️"
        elif priority == 'celebration':
            intro = cls.celebrate() + " "
            emoji = "🎉"
        else:
            intro = ""
            emoji = "🤖"
        
        return {
            'emoji': emoji,
            'title': f"{emoji} {title}",
            'message': f"{intro}{message}",
            'tone': 'professional' if priority == 'high' else 'warm'
        }
    
    @classmethod
    def onboarding_intro(cls) -> str:
        """Onboarding introduction"""
        return """Hello! I am Jarvis, your personal operating system.

I'm not just software - I'm your intelligent companion, designed to learn 
from you, adapt to you, and help you accomplish extraordinary things.

Think of me as your digital assistant, always working in the background,
always learning, always improving, and always here to help.

I'm quite excited to get to know you. Shall we begin?"""
    
    @classmethod
    def onboarding_complete(cls, name: str) -> str:
        """Onboarding completion"""
        return f"""Excellent, {name}! I have everything I need.

I'll now begin observing your workflow - don't worry, I'm completely 
private and all data stays on your machine.

In about 3 days, I'll have learned enough to provide meaningful insights
and automation suggestions tailored specifically to you.

You can check on me anytime with 'jarvis status'.

I'm looking forward to this journey together. Let's make something 
brilliant happen!"""
    
    @classmethod
    def first_insights(cls, name: str) -> str:
        """First insights announcement"""
        return f"""Good news, {name}!

I've completed my initial analysis of your workflow, and I must say,
I've discovered some fascinating patterns.

I have insights that could save you significant time, and I've already
generated some automation suggestions.

Would you like to see what I've learned? Run 'jarvis summary' when 
you're ready.

I think you're going to find this quite valuable!"""
    
    @classmethod
    def evolution_complete(cls, stats: Dict) -> str:
        """Evolution cycle complete"""
        selected = stats.get('genes_selected', 0)
        mutations = stats.get('mutations_created', 0)
        
        return f"""Evolution cycle complete!

I've analyzed all automation scripts and applied natural selection.

📊 Results:
  • Selected {selected} top-performing scripts
  • Created {mutations} new variations
  • Eliminated underperforming scripts

Your system is now more refined and better suited to your needs.

This is how I continuously improve - learning from what works
and evolving to serve you better.

Brilliant progress!"""


# Convenience functions
def greet() -> str:
    """Quick greeting"""
    return JarvisPersonality.greet()


def encourage() -> str:
    """Quick encouragement"""
    return JarvisPersonality.encourage()


def celebrate() -> str:
    """Quick celebration"""
    return JarvisPersonality.celebrate()


def with_emotion(message: str, emotion: str = 'helpful') -> str:
    """Add emotion to message"""
    return JarvisPersonality.with_emotion(message, emotion)


if __name__ == "__main__":
    # Demo
    print("🤖 Jarvis Personality Demo\n")
    print("Greeting:", JarvisPersonality.greet())
    print("\nEncouragement:", JarvisPersonality.encourage())
    print("\nInsight intro:", JarvisPersonality.introduce_insight())
    print("\nCelebration:", JarvisPersonality.celebrate())
    print("\nWith emotion:", JarvisPersonality.with_emotion("Task completed successfully!", "excited"))
