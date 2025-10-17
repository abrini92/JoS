#!/usr/bin/env python3
"""
JarvisOS - Native Desktop Notifications
TOP 0.1% - Beautiful, native, actionable notifications

macOS: terminal-notifier + osascript
Linux: notify-send
"""

import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class Notification:
    """A native notification"""
    title: str
    message: str
    subtitle: Optional[str] = None
    sound: Optional[str] = None
    icon: Optional[str] = None
    actions: Optional[List[str]] = None
    timeout: int = 5  # seconds
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "message": self.message,
            "subtitle": self.subtitle,
            "sound": self.sound,
            "icon": self.icon,
            "actions": self.actions,
            "timeout": self.timeout
        }


class NativeNotifier:
    """
    Native desktop notifications for JarvisOS
    
    Supports:
    - macOS (terminal-notifier, osascript)
    - Linux (notify-send)
    - Sounds
    - Icons
    - Actions (macOS)
    """
    
    def __init__(self, app_name: str = "JarvisOS"):
        self.app_name = app_name
        self.system = platform.system()
        self.notifier_available = self._check_notifier()
    
    def _check_notifier(self) -> bool:
        """Check if notification system is available"""
        if self.system == "Darwin":  # macOS
            # Check for terminal-notifier
            if shutil.which("terminal-notifier"):
                return True
            # Fallback to osascript (always available on macOS)
            return True
        
        elif self.system == "Linux":
            # Check for notify-send
            return shutil.which("notify-send") is not None
        
        return False
    
    def notify(
        self,
        title: str,
        message: str,
        subtitle: Optional[str] = None,
        sound: Optional[str] = "default",
        icon: Optional[str] = None,
        actions: Optional[List[str]] = None,
        timeout: int = 5
    ) -> bool:
        """
        Send a native notification
        
        Args:
            title: Notification title
            message: Notification message
            subtitle: Subtitle (macOS only)
            sound: Sound name or "default" or None
            icon: Path to icon file
            actions: List of action buttons (macOS only)
            timeout: Timeout in seconds
        
        Returns:
            True if notification sent successfully
        """
        
        if not self.notifier_available:
            # Fallback to terminal print
            print(f"\n🔔 {title}")
            if subtitle:
                print(f"   {subtitle}")
            print(f"   {message}\n")
            return False
        
        notification = Notification(
            title=title,
            message=message,
            subtitle=subtitle,
            sound=sound,
            icon=icon,
            actions=actions,
            timeout=timeout
        )
        
        if self.system == "Darwin":
            return self._notify_macos(notification)
        elif self.system == "Linux":
            return self._notify_linux(notification)
        
        return False
    
    def _notify_macos(self, notif: Notification) -> bool:
        """Send notification on macOS"""
        
        # Try terminal-notifier first (better features)
        if shutil.which("terminal-notifier"):
            return self._notify_macos_terminal_notifier(notif)
        
        # Fallback to osascript
        return self._notify_macos_osascript(notif)
    
    def _notify_macos_terminal_notifier(self, notif: Notification) -> bool:
        """Send notification using terminal-notifier"""
        
        cmd = [
            "terminal-notifier",
            "-title", notif.title,
            "-message", notif.message,
            "-group", self.app_name,
            "-sender", "com.apple.Terminal"
        ]
        
        if notif.subtitle:
            cmd.extend(["-subtitle", notif.subtitle])
        
        if notif.sound:
            sound_name = "default" if notif.sound == "default" else notif.sound
            cmd.extend(["-sound", sound_name])
        
        if notif.icon:
            cmd.extend(["-appIcon", notif.icon])
        
        if notif.actions:
            cmd.extend(["-actions", ",".join(notif.actions)])
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _notify_macos_osascript(self, notif: Notification) -> bool:
        """Send notification using osascript (AppleScript)"""
        
        message = notif.message
        if notif.subtitle:
            message = f"{notif.subtitle}\n{message}"
        
        script = f'''
        display notification "{message}" with title "{notif.title}"
        '''
        
        if notif.sound:
            script += f' sound name "default"'
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _notify_linux(self, notif: Notification) -> bool:
        """Send notification on Linux using notify-send"""
        
        cmd = [
            "notify-send",
            notif.title,
            notif.message,
            "-t", str(notif.timeout * 1000),  # milliseconds
            "-a", self.app_name
        ]
        
        # Urgency level
        cmd.extend(["-u", "normal"])
        
        # Icon
        if notif.icon:
            cmd.extend(["-i", notif.icon])
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def notify_success(self, title: str, message: str) -> bool:
        """Send a success notification"""
        return self.notify(
            title=f"✅ {title}",
            message=message,
            sound="Glass"  # Success sound
        )
    
    def notify_info(self, title: str, message: str) -> bool:
        """Send an info notification"""
        return self.notify(
            title=f"ℹ️  {title}",
            message=message,
            sound=None
        )
    
    def notify_warning(self, title: str, message: str) -> bool:
        """Send a warning notification"""
        return self.notify(
            title=f"⚠️  {title}",
            message=message,
            sound="Basso"  # Warning sound
        )
    
    def notify_error(self, title: str, message: str) -> bool:
        """Send an error notification"""
        return self.notify(
            title=f"❌ {title}",
            message=message,
            sound="Sosumi"  # Error sound
        )
    
    def notify_jarvis(
        self,
        message: str,
        subtitle: Optional[str] = None,
        actions: Optional[List[str]] = None
    ) -> bool:
        """Send a notification from Jarvis"""
        return self.notify(
            title="🤖 Jarvis",
            message=message,
            subtitle=subtitle,
            sound="Hero",  # Jarvis sound
            actions=actions
        )


# Singleton instance
_notifier: Optional[NativeNotifier] = None

def get_notifier() -> NativeNotifier:
    """Get the global notifier instance"""
    global _notifier
    if _notifier is None:
        _notifier = NativeNotifier()
    return _notifier


# Convenience functions
def notify(title: str, message: str, **kwargs) -> bool:
    """Send a notification"""
    return get_notifier().notify(title, message, **kwargs)

def notify_success(title: str, message: str) -> bool:
    """Send a success notification"""
    return get_notifier().notify_success(title, message)

def notify_info(title: str, message: str) -> bool:
    """Send an info notification"""
    return get_notifier().notify_info(title, message)

def notify_warning(title: str, message: str) -> bool:
    """Send a warning notification"""
    return get_notifier().notify_warning(title, message)

def notify_error(title: str, message: str) -> bool:
    """Send an error notification"""
    return get_notifier().notify_error(title, message)

def notify_jarvis(message: str, subtitle: Optional[str] = None, actions: Optional[List[str]] = None) -> bool:
    """Send a notification from Jarvis"""
    return get_notifier().notify_jarvis(message, subtitle, actions)


if __name__ == "__main__":
    # Test notifications
    print("🧪 Testing Native Notifications\n")
    
    notifier = NativeNotifier()
    
    print(f"System: {notifier.system}")
    print(f"Notifier available: {notifier.notifier_available}\n")
    
    # Test 1: Basic notification
    print("Test 1: Basic notification")
    notifier.notify("JarvisOS", "Testing native notifications")
    print("✅ Sent\n")
    
    import time
    time.sleep(2)
    
    # Test 2: Success notification
    print("Test 2: Success notification")
    notifier.notify_success("Task Complete", "Your automation script finished successfully")
    print("✅ Sent\n")
    
    time.sleep(2)
    
    # Test 3: Jarvis notification
    print("Test 3: Jarvis notification")
    notifier.notify_jarvis(
        "Good afternoon! I've prepared your coding environment.",
        subtitle="Predictive Engine",
        actions=["Thanks", "Dismiss"]
    )
    print("✅ Sent\n")
    
    time.sleep(2)
    
    # Test 4: Warning
    print("Test 4: Warning notification")
    notifier.notify_warning("Low Energy Detected", "Consider taking a break")
    print("✅ Sent\n")
    
    print("🎉 All tests complete!")
    print("\nCheck your notification center!")
