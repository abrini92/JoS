#!/bin/bash
#
# JarvisOS Desktop Welcome
# Launches automatically when desktop starts
#

# Wait for desktop to be ready
sleep 5

# Open terminal with Jarvis greeting
xfce4-terminal \
    --maximize \
    --title="Jarvis - Your Personal OS" \
    --command="bash -c 'cd /opt/jarvisos && source venv/bin/activate && python jarvis.py greet && echo \"\" && echo \"Type any jarvis command to continue...\" && bash'" \
    --hold &

# Show notification
notify-send "🤖 Jarvis" "Good morning! I'm ready to help you today." -i dialog-information

# Optional: Auto-run status in background
sleep 2
xfce4-terminal \
    --geometry=80x20+50+50 \
    --title="Jarvis Status" \
    --command="bash -c 'cd /opt/jarvisos && source venv/bin/activate && python jarvis.py status && read -p \"Press Enter to close...\"'" &
