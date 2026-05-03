# Daycycle Usage Guide

## Checking Service Status

Since daycycle runs as a **user service** (not system-wide), always use `systemctl --user`:

```bash
# Check if timer is active
systemctl --user status daycycle-wallpaper.timer

# View recent logs
journalctl --user-unit daycycle-wallpaper -n 20

# Enable/disable timer
systemctl --user enable daycycle-wallpaper.timer
systemctl --user disable daycycle-wallpaper.timer
```

## Quick Start

1. **Install**
   ```bash
   ./daycycle-install.sh
   ```

2. **Configure**
   ```bash
   daycycle-config.sh
   ```

3. **Add Images**
   - Drag images into the slots in the settings UI, or
   - Click Browse to select images manually
   - See thumbnails update in the Preview column

4. **Save & Enable**
   - Click Save to store configuration
   - Click "Install/Enable Timer" to start automatic updates

## Settings UI Walkthrough

### Location Settings

**City Name, Region, Timezone**
- Set your geographic location so sunrise/sunset times are accurate
- Example: Chicago, USA, America/Chicago
- Timezone must be in IANA format (e.g., America/New_York)
- Find your timezone: `timedatectl list-timezones`

**Latitude, Longitude**
- Decimal format (positive = North/East, negative = South/West)
- Get from Google Maps: right-click location → copy coordinates
- Example: 41.93, -87.87 (Chicago)

### Image Slots

Each row represents one wallpaper slot (1-6):

**Preview Column**
- Live thumbnail preview of the selected image
- Updates as you browse for images
- Shows actual image content scaled to 120x80 pixels

**Image File Column**
- Path to the wallpaper image
- Drag images from file manager to auto-populate
- Click Browse to open file picker
- Supports JPG, PNG, and most image formats

**Time Rule Column**
- When to switch to this image
- Options:
  - **sunrise** - Switch at local sunrise
  - **sunset** - Switch at local sunset
  - **noon** - Switch at 12:00 PM
  - **midnight** - Switch at 12:00 AM
  - **clock** - Switch at specific time (use Clock HH:MM column)

**Offset min Column**
- Minutes to add/subtract from the rule time
- Example: Rule=sunrise, Offset=-30 → 30 min before sunrise
- Negative values are supported

**Clock HH:MM Column**
- Used when Time Rule is set to "clock"
- Format: HH:MM (24-hour time)
- Example: 06:00 (6 AM), 18:30 (6:30 PM)

### Buttons

**Browse**
- Opens file picker to select an image
- Only works for that slot

**Save**
- Saves all settings to `~/.config/daycycle-wallpaper.conf`
- Changes take effect immediately
- Timer will use new settings on next update

**Install/Enable Timer**
- Sets up systemd to run daycycle-wallpaper.sh every 15 minutes
- Must be done once after initial setup
- Can be disabled with: `systemctl --user disable daycycle-wallpaper.timer`

**Run Now**
- Updates wallpaper immediately with current settings
- Useful for testing before enabling timer

## Common Workflows

### Workflow 1: Basic Setup with Clock Times

If you don't want to use sun positions:

1. Set your location (just for reference)
2. Set Time Rule to "clock" for all slots
3. Set times manually:
   - IMAGE_1 (clock 06:00) - Morning
   - IMAGE_2 (clock 09:00) - Late morning
   - IMAGE_3 (clock 12:00) - Afternoon
   - IMAGE_4 (clock 18:00) - Evening
   - IMAGE_5 (clock 21:00) - Night
   - IMAGE_6 (clock 00:00) - Late night
4. Save and click "Run Now" to test

### Workflow 2: Sun-Based with Offsets

For a more natural progression:

1. Set accurate location (City, Region, Timezone, Lat/Long)
2. Set TIME RULES:
   - IMAGE_1: sunrise, Offset: -120 (2 hrs before sunrise)
   - IMAGE_2: sunrise, Offset: 0
   - IMAGE_3: noon, Offset: -60 (1 hr before noon)
   - IMAGE_4: noon, Offset: 0
   - IMAGE_5: sunset, Offset: 0
   - IMAGE_6: sunset, Offset: 120 (2 hrs after sunset)
3. Select images for each slot
4. Save and enable timer

### Workflow 3: Hybrid (Sun + Clock)

Mix solar events with fixed times for flexibility:

1. Set location
2. Set TIME RULES:
   - IMAGE_1-5: sunrise/sunset with offsets
   - IMAGE_6: clock 23:59 (fixed night image)

## Tips & Tricks

### Getting Good Sunrise/Sunset Data

- Accurate latitude/longitude is crucial
- Get from Google Maps: right-click → copy coordinates
- Format: decimal degrees (41.8781, -87.6298)
- Test with: `python3 daycycle-wallpaper.sh` to see calculated times

### Testing Your Setup

```bash
# Update wallpaper immediately
daycycle-wallpaper.sh

# View the log
journalctl --user -u daycycle-wallpaper.service

# Check next scheduled update
systemctl --user list-timers daycycle-wallpaper.timer
```

### Disabling/Pausing Updates

```bash
# Stop the timer
systemctl --user stop daycycle-wallpaper.timer

# Re-enable later
systemctl --user start daycycle-wallpaper.timer
```

### Finding Good Wallpapers

- Free sources: Unsplash, Pexels, Pixabay, Wallhaven
- Search for "daylight progression", "golden hour", "landscape"
- Resize to 1920x1080 before adding (optional but recommended)

### Image File Paths

- Paths support `~` for home directory
- Example: `~/wallpapers/daycycle/morning.jpg`
- Absolute paths also work: `/home/username/pictures/morning.jpg`

## Command Line Usage

### daycycle-config.sh
Opens the settings GUI (only way to configure)

### daycycle-wallpaper.sh
Updates wallpaper based on current settings

```bash
# Run once
daycycle-wallpaper.sh

# Follow output
daycycle-wallpaper.sh 2>&1 | tee ~/daycycle.log
```

### systemctl commands

```bash
# Check timer status
systemctl --user status daycycle-wallpaper.timer

# View timers
systemctl --user list-timers

# View service status
systemctl --user status daycycle-wallpaper.service

# View logs
journalctl --user -u daycycle-wallpaper.service -f

# Enable/disable timer
systemctl --user enable daycycle-wallpaper.timer
systemctl --user disable daycycle-wallpaper.timer

# Start/stop timer
systemctl --user start daycycle-wallpaper.timer
systemctl --user stop daycycle-wallpaper.timer
```

## Troubleshooting

### Wallpaper doesn't change

**Check 1: Is the timer running?**
```bash
systemctl --user status daycycle-wallpaper.timer
```

**Check 2: View the logs**
```bash
journalctl --user -u daycycle-wallpaper.service -f
```

**Check 3: Test manually**
```bash
daycycle-wallpaper.sh
```

### Settings UI shows "No image" or "Not found"

- Image file path is wrong
- File was deleted
- File permissions prevent reading
- Use Browse button to re-select

### Thumbnails don't show in settings UI

Install the image library:
```bash
sudo apt install python3-pil.imagetk
```

### Drag-and-drop doesn't work

Install tkinterdnd2:
```bash
pip3 install --user tkinterdnd2
```

### Timer runs but wallpaper doesn't update

- Check wallpaper manager supports X11 (some display managers don't support programmatic changes)
- Try manual update: `daycycle-wallpaper.sh` and check if it works
- View logs: `journalctl --user -u daycycle-wallpaper.service`

### Wrong sunrise/sunset times

- Verify latitude/longitude are correct (decimal degrees)
- Check timezone: `timedatectl`
- Example correct timezone: `America/Chicago`
- Wrong timezone causes wrong sun times

## Configuration File

Location: `~/.config/daycycle-wallpaper.conf`

Example:
```ini
WALLDIR=~/wallpapers/daycycle
CITY_NAME=Chicago
REGION=USA
TIMEZONE=America/Chicago
LATITUDE=41.93
LONGITUDE=-87.87
IMAGE_1=~/wallpapers/daycycle/1-morning.jpg
IMAGE_2=~/wallpapers/daycycle/2-late-morning.jpg
IMAGE_3=~/wallpapers/daycycle/3-afternoon.jpg
IMAGE_4=~/wallpapers/daycycle/4-evening.jpg
IMAGE_5=~/wallpapers/daycycle/5-night.jpg
IMAGE_6=~/wallpapers/daycycle/6-late-night.jpg
RULE_1=sunrise
RULE_2=sunrise
RULE_3=noon
RULE_4=sunset
RULE_5=sunset
RULE_6=midnight
OFFSET_MIN_1=0
OFFSET_MIN_2=120
OFFSET_MIN_3=0
OFFSET_MIN_4=-180
OFFSET_MIN_5=0
OFFSET_MIN_6=0
CLOCK_TIME_1=06:00
CLOCK_TIME_2=09:00
CLOCK_TIME_3=12:00
CLOCK_TIME_4=18:00
CLOCK_TIME_5=21:00
CLOCK_TIME_6=00:00
```

You can edit this file manually, but it's recommended to use the GUI.
