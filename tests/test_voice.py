"""
Tests for Voice System (TTS, STT, Jarvis Voice)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from jarvisos.voice.tts import TextToSpeech, get_jarvis_voice
from jarvisos.voice.stt import SpeechToText
from jarvisos.voice.jarvis_voice import JarvisVoice


class TestTextToSpeech:
    """Test TTS system"""
    
    def test_tts_creation(self):
        """Test creating TTS instance"""
        tts = TextToSpeech(engine="auto")
        assert tts is not None
        assert tts.engine in ["macos", "pyttsx3", "gtts", "espeak", "none"]
    
    def test_detect_engines(self):
        """Test engine detection"""
        tts = TextToSpeech()
        engines = tts._detect_engines()
        assert isinstance(engines, list)
    
    def test_get_jarvis_voice(self):
        """Test getting Jarvis voice"""
        voice = get_jarvis_voice(engine="macos", style="default")
        # Should return a voice name or None
        assert voice is None or isinstance(voice, str)
    
    @patch('subprocess.run')
    def test_speak_macos(self, mock_run):
        """Test macOS say command"""
        mock_run.return_value = Mock(returncode=0)
        
        tts = TextToSpeech(engine="macos")
        tts.speak("Hello world")
        
        # Verify subprocess was called
        assert mock_run.called
    
    def test_speak_fallback(self):
        """Test fallback when no engine available"""
        tts = TextToSpeech(engine="none")
        # Should not raise exception
        tts.speak("Hello world")


class TestSpeechToText:
    """Test STT system"""
    
    def test_stt_creation(self):
        """Test creating STT instance"""
        stt = SpeechToText(engine="auto")
        assert stt is not None
        assert stt.engine in ["whisper", "google", "sphinx", "none"]
    
    def test_detect_engines(self):
        """Test engine detection"""
        stt = SpeechToText()
        engines = stt._detect_engines()
        assert isinstance(engines, list)
    
    def test_listen_no_engine(self):
        """Test listening with no engine"""
        stt = SpeechToText(engine="none")
        result = stt.listen(timeout=1)
        # Should return None or empty string
        assert result is None or result == ""


class TestJarvisVoice:
    """Test Jarvis Voice system"""
    
    def test_jarvis_creation(self):
        """Test creating Jarvis instance"""
        jarvis = JarvisVoice(user_name="Test User")
        assert jarvis.user_name == "Test User"
        assert jarvis.tts is not None
        assert jarvis.stt is not None
    
    def test_jarvis_default_user(self):
        """Test default user name"""
        jarvis = JarvisVoice()
        assert jarvis.user_name == "there"
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_speak(self, mock_speak):
        """Test Jarvis speaking"""
        jarvis = JarvisVoice()
        jarvis.speak("Hello")
        
        # Verify TTS was called
        assert mock_speak.called
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_greet(self, mock_speak):
        """Test Jarvis greeting"""
        jarvis = JarvisVoice(user_name="Alice")
        jarvis.greet()
        
        # Should speak a greeting
        assert mock_speak.called
        call_args = str(mock_speak.call_args)
        assert "Alice" in call_args or "Good" in call_args
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_introduce(self, mock_speak):
        """Test Jarvis introduction"""
        jarvis = JarvisVoice()
        jarvis.introduce()
        
        # Should speak introduction
        assert mock_speak.called
        call_args = str(mock_speak.call_args)
        assert "Jarvis" in call_args or "operating system" in call_args.lower()
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_confirm(self, mock_speak):
        """Test Jarvis confirmation"""
        jarvis = JarvisVoice()
        jarvis.confirm("Task completed")
        
        assert mock_speak.called
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_acknowledge(self, mock_speak):
        """Test Jarvis acknowledgment"""
        jarvis = JarvisVoice()
        jarvis.acknowledge()
        
        assert mock_speak.called
    
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_notify(self, mock_speak):
        """Test Jarvis notification"""
        jarvis = JarvisVoice()
        jarvis.notify("System update available")
        
        assert mock_speak.called
    
    @patch.object(SpeechToText, 'listen')
    @patch.object(TextToSpeech, 'speak')
    def test_jarvis_ask_question(self, mock_speak, mock_listen):
        """Test Jarvis asking question"""
        mock_listen.return_value = "Yes"
        
        jarvis = JarvisVoice()
        response = jarvis.ask_question("Do you want to continue?")
        
        assert mock_speak.called
        assert mock_listen.called
        assert response == "Yes"
    
    def test_jarvis_wake_word(self):
        """Test wake word configuration"""
        jarvis = JarvisVoice()
        assert jarvis.wake_word == "hey jarvis"
    
    def test_jarvis_listening_state(self):
        """Test listening state management"""
        jarvis = JarvisVoice()
        assert jarvis.listening == False
        
        # Start listening (won't actually listen in test)
        jarvis.listening = True
        assert jarvis.listening == True
        
        jarvis.stop_listening()
        assert jarvis.listening == False


class TestVoiceIntegration:
    """Integration tests for voice system"""
    
    def test_full_voice_pipeline(self):
        """Test complete voice interaction"""
        jarvis = JarvisVoice(user_name="Test")
        
        # Should not raise exceptions
        jarvis.speak("Test message")
        jarvis.greet()
        jarvis.acknowledge()
    
    def test_voice_with_no_engines(self):
        """Test voice system works even without engines"""
        # This should not crash
        jarvis = JarvisVoice()
        jarvis.speak("Hello")
        result = jarvis.listen(timeout=0.1)
        # Should return None or empty
        assert result is None or result == ""
