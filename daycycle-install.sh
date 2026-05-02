#!/usr/bin/env bash
set -euo pipefail

# Daycycle Wallpaper - Installation Script
# This script installs all dependencies and moves files to appropriate locations

echo "=== Daycycle Wallpaper Installation ==="
echo

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if running on a system with apt (Debian/Ubuntu)
if ! command -v apt &> /dev/null; then
	echo -e "${YELLOW}Warning: apt package manager not found.${NC}"
	echo "This script is designed for Debian/Ubuntu systems."
	echo "You may need to manually install dependencies for your system."
	echo
fi

# Function to check and install package
install_if_missing() {
	local package=$1
	local name=${2:-$package}
	
	if dpkg -l | grep -q "^ii  $package"; then
		echo -e "${GREEN}✓${NC} $name is installed"
	else
		echo -e "${YELLOW}Installing${NC} $name..."
		sudo apt update
		sudo apt install -y "$package"
		echo -e "${GREEN}✓${NC} $name installed"
	fi
}

# Function to check Python module
check_python_module() {
	local module=$1
	local name=${2:-$module}
	local install_cmd=${3:-}
	
	if python3 -c "import $module" >/dev/null 2>&1; then
		echo -e "${GREEN}✓${NC} Python $name is available"
		return 0
	else
		echo -e "${YELLOW}✗${NC} Python $name is missing"
		if [ -n "$install_cmd" ]; then
			echo "  Installing with: $install_cmd"
			eval "$install_cmd"
			echo -e "${GREEN}✓${NC} Python $name installed"
		fi
		return 1
	fi
}

echo "Checking system dependencies..."
echo

# Check for Python 3
if ! command -v python3 &> /dev/null; then
	echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
	echo "Install it with: sudo apt install -y python3"
	exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 is installed"

# Check for pip3
if ! command -v pip3 &> /dev/null; then
	echo -e "${YELLOW}Installing${NC} pip3..."
	sudo apt update
	sudo apt install -y python3-pip
	echo -e "${GREEN}✓${NC} pip3 installed"
else
	echo -e "${GREEN}✓${NC} pip3 is installed"
fi

echo

# Install Python dependencies
echo "Checking Python dependencies..."
check_python_module "tkinter" "tkinter" "sudo apt install -y python3-tk"

# ImageTk for thumbnail support
if ! python3 -c 'from PIL import ImageTk' >/dev/null 2>&1; then
	echo -e "${YELLOW}Installing${NC} python3-pil.imagetk for thumbnail support..."
	sudo apt update
	sudo apt install -y python3-pil.imagetk
	echo -e "${GREEN}✓${NC} python3-pil.imagetk installed"
else
	echo -e "${GREEN}✓${NC} python3-pil.imagetk is installed"
fi

# tkinterdnd2 is optional but recommended
echo
echo "Checking optional Python dependencies..."
if check_python_module "tkinterdnd2" "tkinterdnd2" "pip3 install --user tkinterdnd2"; then
	echo -e "${GREEN}✓${NC} Drag-and-drop support will be available"
else
	echo -e "${YELLOW}Note:${NC} Drag-and-drop is disabled. Enable it with: pip3 install --user tkinterdnd2"
fi

# Pillow for thumbnails
echo
if check_python_module "PIL" "Pillow" "pip3 install --user Pillow"; then
	echo -e "${GREEN}✓${NC} Thumbnail previews will be available"
else
	echo -e "${YELLOW}Note:${NC} Thumbnail previews are disabled. Enable it with: pip3 install --user Pillow"
fi

echo
echo "Installing files to appropriate locations..."
echo

# Create directories
mkdir -p "$HOME/bin"
mkdir -p "$HOME/.config/systemd/user"
mkdir -p "$HOME/wallpapers/daycycle"

# Copy executable scripts to ~/bin
cp "$SCRIPT_DIR/daycycle-settings.py" "$HOME/bin/daycycle-settings.py"
cp "$SCRIPT_DIR/daycycle-wallpaper.sh" "$HOME/bin/daycycle-wallpaper.sh"
cp "$SCRIPT_DIR/daycycle-config.sh" "$HOME/bin/daycycle-config.sh"
chmod +x "$HOME/bin/daycycle-settings.py"
chmod +x "$HOME/bin/daycycle-wallpaper.sh"
chmod +x "$HOME/bin/daycycle-config.sh"
echo -e "${GREEN}✓${NC} Copied scripts to $HOME/bin"

# Copy systemd files
cp "$SCRIPT_DIR/daycycle-wallpaper.service" "$HOME/.config/systemd/user/daycycle-wallpaper.service"
cp "$SCRIPT_DIR/daycycle-wallpaper.timer" "$HOME/.config/systemd/user/daycycle-wallpaper.timer"
echo -e "${GREEN}✓${NC} Copied systemd service and timer to $HOME/.config/systemd/user"

echo
echo "Setting up systemd timer..."
echo

# Reload systemd user daemon
systemctl --user daemon-reload

# Ask if user wants to enable the timer
read -p "Enable and start daycycle-wallpaper timer? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	systemctl --user enable daycycle-wallpaper.timer
	systemctl --user start daycycle-wallpaper.timer
	echo -e "${GREEN}✓${NC} Timer enabled and started"
	echo "Check status with: systemctl --user status daycycle-wallpaper.timer"
else
	echo "Skipped. You can enable later with: systemctl --user enable --now daycycle-wallpaper.timer"
fi

echo
echo -e "${GREEN}=== Installation Complete ===${NC}"
echo
echo "Next steps:"
echo "1. Add wallpaper images to $HOME/wallpapers/daycycle/"
echo "2. Run daycycle-settings.py to configure your location and wallpaper schedule"
echo "   or run: $HOME/bin/daycycle-settings.py"
echo
