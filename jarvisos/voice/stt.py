"""
JarvisOS Speech-to-Text System
Converts speech to text
"""

import subprocess
from typing import Optional, Callable

from ..utils.logger import get_logger

logger = get_logger("jarvisos.voice.stt")


class SpeechToText:
    """Speech-to-Text engine"""
    
    def __init__(self, engine: str = "auto"):
        """
        Initialize STT engine
        
        Args:
            engine: STT engine to use ('auto', 'whisper', 'google', 'sphinx')
        """
        self.engine = engine
        self.available_engines = self._detect_engines()
        
        if engine == "auto":
            self.engine = self._select_best_engine()
        
        logger.info(f"STT initialized with engine: {self.engine}")
    
    def _detect_engines(self) -> list:
        """Detect available STT engines"""
        engines = []
        
        # Whisper (OpenAI, best quality)
        try:
            import whisper
            engines.append('whisper')
        except ImportError:
            pass
        
        # SpeechRecognition (Google, requires internet)
        try:
            import speech_recognition
            engines.append('google')
        except ImportError:
            pass
        
        # PocketSphinx (offline, lower quality)
        try:
            import speech_recognition
            import pocketsphinx
            engines.append('sphinx')
        except ImportError:
            pass
        
        logger.debug(f"Available STT engines: {engines}")
        return engines
    
    def _select_best_engine(self) -> str:
        """Select best available engine"""
        priority = ['whisper', 'google', 'sphinx']
        
        for engine in priority:
            if engine in self.available_engines:
                return engine
        
        logger.warning("No STT engine available")
        return 'none'
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for speech and convert to text
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for phrase
            
        Returns:
            Transcribed text or None
        """
        logger.info("Listening for speech...")
        
        try:
            if self.engine == 'whisper':
                return self._listen_whisper(timeout, phrase_time_limit)
            elif self.engine == 'google':
                return self._listen_google(timeout, phrase_time_limit)
            elif self.engine == 'sphinx':
                return self._listen_sphinx(timeout, phrase_time_limit)
            else:
                logger.warning(f"STT engine '{self.engine}' not available")
                return None
        except Exception as e:
            logger.error(f"STT failed: {e}")
            return None
    
    def _listen_whisper(self, timeout: int, phrase_time_limit: int) -> Optional[str]:
        """Listen using Whisper (best quality)"""
        import speech_recognition as sr
        import whisper
        
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            logger.debug("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.debug("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        
        # Save audio to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio.get_wav_data())
            temp_file = f.name
        
        # Transcribe with Whisper
        model = whisper.load_model("base")
        result = model.transcribe(temp_file)
        
        # Cleanup
        import os
        os.remove(temp_file)
        
        text = result['text'].strip()
        logger.info(f"Transcribed: {text}")
        return text
    
    def _listen_google(self, timeout: int, phrase_time_limit: int) -> Optional[str]:
        """Listen using Google Speech Recognition"""
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            logger.debug("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.debug("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        
        try:
            text = recognizer.recognize_google(audio)
            logger.info(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Google API error: {e}")
            return None
    
    def _listen_sphinx(self, timeout: int, phrase_time_limit: int) -> Optional[str]:
        """Listen using PocketSphinx (offline)"""
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            logger.debug("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.debug("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        
        try:
            text = recognizer.recognize_sphinx(audio)
            logger.info(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Sphinx error: {e}")
            return None
    
    def listen_for_wake_word(
        self,
        wake_word: str = "hey jarvis",
        callback: Optional[Callable] = None,
        timeout: int = 5
    ) -> bool:
        """
        Listen for wake word
        
        Args:
            wake_word: Wake word to detect
            callback: Function to call when wake word detected
            timeout: Timeout in seconds
            
        Returns:
            True if wake word detected
        """
        text = self.listen(timeout=timeout)
        
        if text and wake_word.lower() in text.lower():
            logger.info(f"Wake word detected: {wake_word}")
            if callback:
                callback()
            return True
        
        return False


# Example usage
if __name__ == "__main__":
    stt = SpeechToText()
    
    print("Available engines:", stt.available_engines)
    print("Selected engine:", stt.engine)
    
    if stt.engine != 'none':
        print("\nSay something...")
        text = stt.listen()
        
        if text:
            print(f"You said: {text}")
        else:
            print("No speech detected")
