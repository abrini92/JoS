#!/usr/bin/env python3
"""
JarvisOS - System Tray Integration
TOP 0.1% - Menu bar icon with quick actions

macOS: rumps (Ridiculously Uncomplicated macOS Python Statusbar apps)
Linux: pystray
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional, Callable
import threading

# Try to import system tray libraries
TRAY_AVAILABLE = False
SYSTEM = sys.platform

if SYSTEM == "darwin":  # macOS
    try:
        import rumps
        TRAY_AVAILABLE = True
        TRAY_LIBRARY = "rumps"
    except ImportError:
        TRAY_LIBRARY = None
elif SYSTEM.startswith("linux"):
    try:
        import pystray
        from PIL import Image, ImageDraw
        TRAY_AVAILABLE = True
        TRAY_LIBRARY = "pystray"
    except ImportError:
        TRAY_LIBRARY = None


class JarvisSystemTray:
    """
    System tray icon for JarvisOS
    
    Provides quick access to:
    - Status
    - Predictions
    - Settings
    - Quit
    """
    
    def __init__(self, app_name: str = "JarvisOS"):
        self.app_name = app_name
        self.available = TRAY_AVAILABLE
        self.library = TRAY_LIBRARY
        self.app = None
        self.icon = None
    
    def create_macos_app(self):
        """Create macOS menu bar app using rumps"""
        if not TRAY_AVAILABLE or TRAY_LIBRARY != "rumps":
            return None
        
        class JarvisApp(rumps.App):
            def __init__(self, parent):
                super().__init__(
                    "🤖",  # Icon (emoji for now)
                    title="Jarvis",
                    quit_button=None  # Custom quit
                )
                self.parent = parent
                
                # Menu items
                self.menu = [
                    rumps.MenuItem("Status", callback=self.show_status),
                    rumps.MenuItem("Predictions", callback=self.show_predictions),
                    None,  # Separator
                    rumps.MenuItem("Settings", callback=self.show_settings),
                    None,
                    rumps.MenuItem("Quit Jarvis", callback=self.quit_app)
                ]
            
            def show_status(self, _):
                """Show status"""
                subprocess.run(["python", "jarvis.py", "status"])
            
            def show_predictions(self, _):
                """Show predictions"""
                subprocess.run(["python", "jarvis.py", "predict"])
            
            def show_settings(self, _):
                """Show settings"""
                rumps.alert("Settings", "Settings coming soon!")
            
            def quit_app(self, _):
                """Quit application"""
                rumps.quit_application()
        
        return JarvisApp(self)
    
    def create_linux_icon(self):
        """Create Linux system tray icon using pystray"""
        if not TRAY_AVAILABLE or TRAY_LIBRARY != "pystray":
            return None
        
        # Create icon image
        def create_image():
            # Simple circle icon
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), 'white')
            dc = ImageDraw.Draw(image)
            dc.ellipse([16, 16, 48, 48], fill='blue', outline='darkblue')
            return image
        
        # Menu items
        def on_status(icon, item):
            subprocess.run(["python", "jarvis.py", "status"])
        
        def on_predictions(icon, item):
            subprocess.run(["python", "jarvis.py", "predict"])
        
        def on_quit(icon, item):
            icon.stop()
        
        menu = pystray.Menu(
            pystray.MenuItem("Status", on_status),
            pystray.MenuItem("Predictions", on_predictions),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", on_quit)
        )
        
        icon = pystray.Icon(
            "jarvis",
            create_image(),
            "JarvisOS",
            menu
        )
        
        return icon
    
    def run(self):
        """Run the system tray application"""
        if not self.available:
            print(f"System tray not available on {SYSTEM}")
            print("Install dependencies:")
            if SYSTEM == "darwin":
                print("  pip install rumps")
            elif SYSTEM.startswith("linux"):
                print("  pip install pystray pillow")
            return
        
        if SYSTEM == "darwin":
            self.app = self.create_macos_app()
            if self.app:
                print("🚀 Starting JarvisOS menu bar app...")
                self.app.run()
        
        elif SYSTEM.startswith("linux"):
            self.icon = self.create_linux_icon()
            if self.icon:
                print("🚀 Starting JarvisOS system tray...")
                self.icon.run()
    
    def run_background(self):
        """Run system tray in background thread"""
        if not self.available:
            return
        
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread


def main():
    """Main entry point for system tray"""
    tray = JarvisSystemTray()
    
    if not tray.available:
        print("❌ System tray not available")
        print(f"System: {SYSTEM}")
        print(f"Library: {TRAY_LIBRARY}")
        print("\nInstall dependencies:")
        if SYSTEM == "darwin":
            print("  pip install rumps")
        elif SYSTEM.startswith("linux"):
            print("  pip install pystray pillow")
        return
    
    print(f"✅ System tray available ({TRAY_LIBRARY})")
    print("Starting JarvisOS system tray...")
    print("Press Ctrl+C to stop\n")
    
    try:
        tray.run()
    except KeyboardInterrupt:
        print("\n\n👋 Jarvis system tray stopped")


if __name__ == "__main__":
    main()
