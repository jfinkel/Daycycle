#!/usr/bin/env bash
set -euo pipefail

# Daycycle Wallpaper - Configuration Script
# This runs the settings UI to configure wallpaper schedule and location

# Check dependencies
if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
	echo "Missing Python Tk support (tkinter)." >&2
	echo "Install it with: sudo apt update && sudo apt install -y python3-tk" >&2
	exit 1
fi

if ! python3 -c 'import tkinterdnd2' >/dev/null 2>&1; then
	echo "Note: drag-and-drop is disabled until tkinterdnd2 is installed." >&2
	echo "Enable it with: pip3 install --user tkinterdnd2" >&2
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create bin directory if needed
mkdir -p "$HOME/bin"

# Install scripts if not already there
if [ ! -f "$HOME/bin/daycycle-settings.py" ]; then
	cp "$SCRIPT_DIR/daycycle-settings.py" "$HOME/bin/daycycle-settings.py"
	chmod +x "$HOME/bin/daycycle-settings.py"
fi

# Run settings UI
"$HOME/bin/daycycle-settings.py"
