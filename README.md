# Daycycle Wallpaper

Automatically change your desktop wallpaper based on the sun's position throughout the day. Daycycle uses your location and current time to update your background to match the natural light cycle—sunrise, morning, noon, afternoon, sunset, evening, and night.

## Features

- 🌅 **Sun-position-based wallpaper switching** - Changes images at sunrise, sunset, noon, and other solar events
- 🕐 **Clock-based fallback** - Set specific times if solar data isn't available
- 🗺️ **Location-aware** - Automatically calculate sunrise/sunset for your timezone
- 🖼️ **6 customizable image slots** - One for each major time of day
- 👁️ **Live preview thumbnails** - See your images in the settings UI before saving
- 🎯 **Drag-and-drop image selection** - Quick setup with visual feedback
- ⚙️ **Systemd integration** - Runs automatically via timer (every 15 minutes)
- 📦 **Zero dependencies** - Works with just Python 3 and standard system tools
- 🔄 **Graceful degradation** - Features work without optional packages

## Installation

### Prerequisites
- Linux with systemd support
- Python 3.9+
- X11 or Wayland display server

### Quick Install

```bash
git clone https://github.com/jrfinkel/daycycle.git
cd daycycle
./daycycle-install.sh
```

The installer will:
1. Check for Python 3 and pip
2. Install optional dependencies (PIL for image thumbnails, tkinterdnd2 for drag-and-drop)
3. Copy scripts to `~/bin`
4. Set up systemd timer
5. Create wallpaper directory

### Manual Setup

If you prefer not to run the installer:

```bash
# Copy scripts
mkdir -p ~/bin
cp daycycle-wallpaper.sh ~/bin/
cp daycycle-config.sh ~/bin/
chmod +x ~/bin/daycycle-*.sh

# Create wallpaper directory
mkdir -p ~/wallpapers/daycycle

# Set up systemd
mkdir -p ~/.config/systemd/user
cp daycycle-wallpaper.service ~/.config/systemd/user/
cp daycycle-wallpaper.timer ~/.config/systemd/user/

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now daycycle-wallpaper.timer
```

## Usage

### Configure Wallpapers

Run the settings UI:

```bash
daycycle-config.sh
```

Or directly:

```bash
python3 ~/bin/daycycle-settings.py
```

In the settings window:
1. **Set your location** - City, region, timezone (Chicago, USA, America/Chicago by default)
2. **Set your images** - Drag images or click Browse to select wallpapers for each time slot
3. **Adjust timing rules** - Choose sunrise/sunset/noon/clock for each slot
4. **Save** - Click Save to store configuration
5. **Enable timer** - Click "Install/Enable Timer" to activate automatic updates

### Manual Wallpaper Update

Update wallpaper immediately without waiting for the timer:

```bash
daycycle-wallpaper.sh
```

### Check Status

View systemd timer status:

```bash
systemctl --user status daycycle-wallpaper.timer
systemctl --user status daycycle-wallpaper.service
```

View logs:

```bash
journalctl --user -u daycycle-wallpaper.service -f
```

## Configuration

Configuration is stored in `~/.config/daycycle-wallpaper.conf`

Example config:

```ini
WALLDIR=~/wallpapers/daycycle
CITY_NAME=Chicago
REGION=USA
TIMEZONE=America/Chicago
LATITUDE=41.93
LONGITUDE=-87.87
IMAGE_1=~/wallpapers/daycycle/1-morning.jpg
RULE_1=sunrise
OFFSET_MIN_1=0
CLOCK_TIME_1=06:00
```

### Time Rules

- **sunrise** - Uses local sunrise time + optional offset
- **sunset** - Uses local sunset time + optional offset
- **noon** - Uses 12:00 PM + optional offset
- **midnight** - Uses 12:00 AM + optional offset
- **clock** - Uses fixed time (HH:MM format)

### Offset Minutes

Add or subtract minutes from the base time. Negative numbers are supported.

Example: `OFFSET_MIN_1=-30` triggers 30 minutes before sunrise

## Image Requirements

- Format: JPG, PNG, or any format supported by PIL
- Recommended resolution: 1920x1080 or higher
- Aspect ratio: 16:9 (will work with others, may be letterboxed)
- File size: <5 MB for best performance

## Optional Dependencies

Install for enhanced features:

```bash
# Image thumbnails in settings UI
sudo apt install python3-pil.imagetk

# Drag-and-drop support
pip3 install --user tkinterdnd2
```

## Troubleshooting

### Wallpaper isn't changing
- Check timer status: `systemctl --user status daycycle-wallpaper.timer`
- Check logs: `journalctl --user -u daycycle-wallpaper.service -f`
- Ensure images exist and paths are correct in settings

### Settings UI doesn't show thumbnails
- Install PIL: `sudo apt install python3-pil.imagetk`
- Restart settings UI

### Location/timezone not working
- Verify timezone format: `timedatectl list-timezones | grep Chicago`
- Verify latitude/longitude are valid (use Google Maps)

### Timer not starting
- Reload systemd: `systemctl --user daemon-reload`
- Enable timer: `systemctl --user enable --now daycycle-wallpaper.timer`

## Files

```
daycycle-wallpaper.sh       Main script that updates wallpaper
daycycle-settings.py        GUI settings application
daycycle-config.sh          Launcher script for settings UI
daycycle-install.sh         Dependency installer and setup
daycycle-wallpaper.service  Systemd service unit
daycycle-wallpaper.timer    Systemd timer unit
```

## Requirements Met

✅ Automatically updates wallpaper based on time  
✅ Sun position aware (sunrise/sunset/noon)  
✅ GUI settings with preview  
✅ Systemd integration  
✅ Cross-timezone support  
✅ Drag-and-drop image selection  
✅ Graceful degradation for missing dependencies  

## Future Ideas

- [ ] Support for multiple monitors
- [ ] Smooth fade transitions between wallpapers
- [ ] Integration with music/activity detection
- [ ] Custom time rules and scheduling
- [ ] Wallpaper collection management
- [ ] Support for other display managers (Wayland, KDE, GNOME-specific)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please see CONTRIBUTING.md

## Author

Created by Joel - [your contact info]

## Support

Found a bug? Have a feature request? Please open an issue on GitHub.
