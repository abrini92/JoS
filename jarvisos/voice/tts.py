"""
JarvisOS Text-to-Speech System
Converts text to natural speech
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger

logger = get_logger("jarvisos.voice.tts")


class TextToSpeech:
    """Text-to-Speech engine"""
    
    def __init__(self, engine: str = "auto"):
        """
        Initialize TTS engine
        
        Args:
            engine: TTS engine to use ('auto', 'macos', 'pyttsx3', 'gtts')
        """
        self.engine = engine
        self.available_engines = self._detect_engines()
        
        if engine == "auto":
            self.engine = self._select_best_engine()
        
        logger.info(f"TTS initialized with engine: {self.engine}")
    
    def _detect_engines(self) -> list:
        """Detect available TTS engines"""
        engines = []
        
        # macOS say command
        if subprocess.run(['which', 'say'], capture_output=True).returncode == 0:
            engines.append('macos')
        
        # pyttsx3 (cross-platform)
        try:
            import pyttsx3
            engines.append('pyttsx3')
        except ImportError:
            pass
        
        # gTTS (Google TTS, requires internet)
        try:
            import gtts
            engines.append('gtts')
        except ImportError:
            pass
        
        # espeak (Linux)
        if subprocess.run(['which', 'espeak'], capture_output=True).returncode == 0:
            engines.append('espeak')
        
        logger.debug(f"Available TTS engines: {engines}")
        return engines
    
    def _select_best_engine(self) -> str:
        """Select best available engine"""
        priority = ['macos', 'pyttsx3', 'gtts', 'espeak']
        
        for engine in priority:
            if engine in self.available_engines:
                return engine
        
        logger.warning("No TTS engine available, using fallback")
        return 'none'
    
    def speak(self, text: str, voice: Optional[str] = None, rate: int = 175):
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
            voice: Voice name (engine-specific)
            rate: Speech rate (words per minute)
        """
        if not text:
            return
        
        logger.info(f"Speaking: {text[:50]}...")
        
        try:
            if self.engine == 'macos':
                self._speak_macos(text, voice, rate)
            elif self.engine == 'pyttsx3':
                self._speak_pyttsx3(text, voice, rate)
            elif self.engine == 'gtts':
                self._speak_gtts(text)
            elif self.engine == 'espeak':
                self._speak_espeak(text, rate)
            else:
                logger.warning(f"TTS engine '{self.engine}' not available")
        except Exception as e:
            logger.error(f"TTS failed: {e}")
    
    def _speak_macos(self, text: str, voice: Optional[str], rate: int):
        """Speak using macOS 'say' command"""
        cmd = ['say']
        
        if voice:
            cmd.extend(['-v', voice])
        
        # Convert rate to macOS format (words per minute)
        cmd.extend(['-r', str(rate)])
        
        cmd.append(text)
        
        subprocess.run(cmd, check=True)
    
    def _speak_pyttsx3(self, text: str, voice: Optional[str], rate: int):
        """Speak using pyttsx3"""
        import pyttsx3
        
        engine = pyttsx3.init()
        
        if voice:
            engine.setProperty('voice', voice)
        
        engine.setProperty('rate', rate)
        engine.say(text)
        engine.runAndWait()
    
    def _speak_gtts(self, text: str):
        """Speak using Google TTS"""
        from gtts import gTTS
        import tempfile
        
        # Generate speech
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            temp_file = f.name
            tts.save(temp_file)
        
        # Play audio
        if subprocess.run(['which', 'afplay'], capture_output=True).returncode == 0:
            # macOS
            subprocess.run(['afplay', temp_file])
        elif subprocess.run(['which', 'mpg123'], capture_output=True).returncode == 0:
            # Linux
            subprocess.run(['mpg123', temp_file])
        
        # Cleanup
        os.remove(temp_file)
    
    def _speak_espeak(self, text: str, rate: int):
        """Speak using espeak (Linux)"""
        subprocess.run(['espeak', '-s', str(rate), text])
    
    def get_voices(self) -> list:
        """Get available voices for current engine"""
        if self.engine == 'macos':
            result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
            voices = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    voice_name = line.split()[0]
                    voices.append(voice_name)
            return voices
        
        elif self.engine == 'pyttsx3':
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            return [v.name for v in voices]
        
        return []


# Jarvis personality presets
JARVIS_VOICES = {
    'macos': {
        'default': 'Alex',
        'british': 'Daniel',
        'female': 'Samantha',
        'deep': 'Fred'
    },
    'pyttsx3': {
        'default': None  # Use system default
    }
}


def get_jarvis_voice(engine: str = 'macos', style: str = 'default') -> Optional[str]:
    """Get Jarvis voice for specific engine and style"""
    return JARVIS_VOICES.get(engine, {}).get(style)


# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    
    print("Available engines:", tts.available_engines)
    print("Selected engine:", tts.engine)
    
    # Test speech
    tts.speak("Hello. I am Jarvis. Your personal operating system.")
    
    # List voices
    voices = tts.get_voices()
    if voices:
        print(f"\nAvailable voices ({len(voices)}):")
        for voice in voices[:5]:
            print(f"  - {voice}")
