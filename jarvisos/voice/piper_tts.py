#!/usr/bin/env python3
"""
JarvisOS - Piper TTS Integration
Better voice quality while staying 100% local
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

class PiperTTS:
    """
    Piper TTS: Neural text-to-speech that's fast and local
    
    Advantages over pyttsx3:
    - Better voice quality (7/10 vs 5/10)
    - Natural sounding
    - Still 100% local
    - Fast inference
    
    Fallback to pyttsx3 if Piper not available
    """
    
    def __init__(self):
        self.available = self._check_piper()
        self.model_path = Path.home() / ".jarvisos" / "piper" / "models"
        self.piper_bin = self._find_piper()
        
        if self.available and not self._has_model():
            self._download_default_model()
    
    def _find_piper(self) -> Optional[str]:
        """Find piper binary"""
        # Check common locations
        locations = [
            "/usr/local/bin/piper",
            "/usr/bin/piper",
            str(Path.home() / ".local" / "bin" / "piper"),
            str(Path.home() / "JoS" / "bin" / "piper"),
        ]
        
        for loc in locations:
            if os.path.exists(loc) and os.access(loc, os.X_OK):
                return loc
        
        # Check PATH
        try:
            result = subprocess.run(
                ["which", "piper"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def _check_piper(self) -> bool:
        """Check if Piper is available"""
        piper = self._find_piper()
        if not piper:
            return False
        
        try:
            result = subprocess.run(
                [piper, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _has_model(self) -> bool:
        """Check if a model is downloaded"""
        if not self.model_path.exists():
            return False
        
        # Check for any .onnx model files
        models = list(self.model_path.glob("*.onnx"))
        return len(models) > 0
    
    def _download_default_model(self):
        """Download default English model (medium quality, ~50MB)"""
        try:
            print("📥 Downloading Piper TTS model (en_US-lessac-medium, ~50MB)...")
            print("   This is a one-time download...")
            
            self.model_path.mkdir(parents=True, exist_ok=True)
            
            # Download from Piper releases
            model_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
            config_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
            
            model_file = self.model_path / "en_US-lessac-medium.onnx"
            config_file = self.model_path / "en_US-lessac-medium.onnx.json"
            
            # Download model
            subprocess.run(
                ["curl", "-L", "-o", str(model_file), model_url],
                check=True,
                capture_output=True,
                timeout=300
            )
            
            # Download config
            subprocess.run(
                ["curl", "-L", "-o", str(config_file), config_url],
                check=True,
                capture_output=True,
                timeout=60
            )
            
            print("   ✅ Model downloaded successfully!")
            
        except Exception as e:
            print(f"   ⚠️  Model download failed: {e}")
            print("   Will use pyttsx3 fallback")
    
    def speak(self, text: str, output_file: Optional[str] = None) -> bool:
        """
        Speak text using Piper TTS
        
        Args:
            text: Text to speak
            output_file: Optional output WAV file path
        
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False
        
        if not self._has_model():
            return False
        
        try:
            # Find model file
            model_file = list(self.model_path.glob("*.onnx"))[0]
            
            # Create temp file if no output specified
            if not output_file:
                fd, output_file = tempfile.mkstemp(suffix=".wav")
                os.close(fd)
                temp_output = True
            else:
                temp_output = False
            
            # Run Piper
            process = subprocess.Popen(
                [self.piper_bin, "--model", str(model_file), "--output_file", output_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text, timeout=30)
            
            if process.returncode != 0:
                return False
            
            # Play the audio if temp file
            if temp_output:
                self._play_audio(output_file)
                os.unlink(output_file)
            
            return True
            
        except Exception as e:
            return False
    
    def _play_audio(self, audio_file: str):
        """Play audio file using system player"""
        try:
            # Try different players
            players = ["aplay", "paplay", "ffplay", "mpv", "mplayer"]
            
            for player in players:
                try:
                    subprocess.run(
                        [player, audio_file],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                    return
                except:
                    continue
            
        except:
            pass


# Singleton
_piper_tts: Optional[PiperTTS] = None

def get_piper_tts() -> PiperTTS:
    """Get Piper TTS instance (singleton)"""
    global _piper_tts
    if _piper_tts is None:
        _piper_tts = PiperTTS()
    return _piper_tts


def is_piper_available() -> bool:
    """Check if Piper TTS is available"""
    return get_piper_tts().available


# Test
if __name__ == "__main__":
    tts = get_piper_tts()
    
    if tts.available:
        print("✅ Piper TTS available")
        print(f"   Binary: {tts.piper_bin}")
        print(f"   Models: {tts.model_path}")
        
        if tts._has_model():
            print("   Testing speech...")
            if tts.speak("Hello from JarvisOS with Piper TTS!"):
                print("   ✅ Speech test successful!")
            else:
                print("   ❌ Speech test failed")
        else:
            print("   ⚠️  No models downloaded")
    else:
        print("❌ Piper TTS not available")
        print("   Install: See install.sh")
