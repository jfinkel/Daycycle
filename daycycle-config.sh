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

# Find the source directory (where the original scripts are)
# First try to find it via package manager, or use development location
if [ -d "$HOME/Programming/Daycycle" ]; then
	SOURCE_DIR="$HOME/Programming/Daycycle"
else
	SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# Run settings UI directly from source (always latest version)
python3 -u "$SOURCE_DIR/daycycle-settings.py"
