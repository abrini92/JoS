#!/bin/bash
#
# Setup JarvisOS Desktop Theme
#

echo "🎨 Setting up JarvisOS Desktop Theme..."

# Set dark theme
xfconf-query -c xsettings -p /Net/ThemeName -s "Adwaita-dark"

# Set terminal colors (Arc Reactor Blue theme)
mkdir -p ~/.config/xfce4/terminal
cat > ~/.config/xfce4/terminal/terminalrc << 'EOF'
[Configuration]
ColorForeground=#00d9ff
ColorBackground=#0a0e14
ColorCursor=#00d9ff
ColorPalette=#0a0e14;#ff3333;#00d9ff;#ffb454;#59c2ff;#c792ea;#95e6cb;#ffffff;#4d5566;#ff6666;#5ccfe6;#ffcc66;#73d0ff;#d4bfff;#aed581;#ffffff
FontName=Monospace 11
MiscAlwaysShowTabs=FALSE
MiscBell=FALSE
MiscBellUrgent=FALSE
MiscBordersDefault=TRUE
MiscCursorBlinks=TRUE
MiscCursorShape=TERMINAL_CURSOR_SHAPE_BLOCK
MiscDefaultGeometry=100x30
MiscInheritGeometry=FALSE
MiscMenubarDefault=FALSE
MiscMouseAutohide=FALSE
MiscMouseWheelZoom=TRUE
MiscToolbarDefault=FALSE
MiscConfirmClose=FALSE
MiscCycleTabs=TRUE
MiscTabCloseButtons=TRUE
MiscTabCloseMiddleClick=TRUE
MiscTabPosition=GTK_POS_TOP
MiscHighlightUrls=TRUE
MiscMiddleClickOpensUri=FALSE
MiscCopyOnSelect=FALSE
MiscShowRelaunchDialog=TRUE
MiscRewrapOnResize=TRUE
MiscUseShiftArrowsToScroll=FALSE
MiscSlimTabs=FALSE
MiscNewTabAdjacent=FALSE
ScrollingBar=TERMINAL_SCROLLBAR_NONE
EOF

# Create desktop shortcut
cat > ~/Desktop/Jarvis.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Jarvis Terminal
Comment=Open Jarvis OS Terminal
Exec=xfce4-terminal --title="Jarvis" --command="bash -c 'cd /opt/jarvisos && source venv/bin/activate && python jarvis.py status && bash'"
Icon=utilities-terminal
Terminal=false
Categories=System;
EOF

chmod +x ~/Desktop/Jarvis.desktop

# Set panel to dark
xfconf-query -c xfce4-panel -p /panels/dark-mode -s true 2>/dev/null || true

echo "✅ Desktop theme configured!"
echo ""
echo "🤖 JarvisOS Desktop Ready!"
echo "   - Dark theme enabled"
echo "   - Arc Reactor Blue colors"
echo "   - Jarvis shortcut on desktop"
echo ""
