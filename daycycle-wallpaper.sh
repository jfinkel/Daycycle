#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="$HOME/.config/daycycle-wallpaper.conf"

WALLDIR="$HOME/wallpapers/daycycle"

# Edit these for the user's location
CITY_NAME="Chicago"
REGION="USA"
TIMEZONE="America/Chicago"
LATITUDE="41.93"
LONGITUDE="-87.87"

# Default images and schedule rules for six slots.
IMAGE_1="$WALLDIR/1-morning.jpg"
IMAGE_2="$WALLDIR/2-late-morning.jpg"
IMAGE_3="$WALLDIR/3-afternoon.jpg"
IMAGE_4="$WALLDIR/4-evening.jpg"
IMAGE_5="$WALLDIR/5-night.jpg"
IMAGE_6="$WALLDIR/6-late-night.jpg"

RULE_1="sunrise"
RULE_2="sunrise"
RULE_3="noon"
RULE_4="sunset"
RULE_5="sunset"
RULE_6="midnight"

OFFSET_MIN_1="0"
OFFSET_MIN_2="120"
OFFSET_MIN_3="0"
OFFSET_MIN_4="-180"
OFFSET_MIN_5="0"
OFFSET_MIN_6="0"

CLOCK_TIME_1="06:00"
CLOCK_TIME_2="09:00"
CLOCK_TIME_3="12:00"
CLOCK_TIME_4="18:00"
CLOCK_TIME_5="21:00"
CLOCK_TIME_6="00:00"

# Load user overrides written by the Settings GUI.
if [ -f "$CONFIG_FILE" ]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
fi

export CITY_NAME REGION TIMEZONE LATITUDE LONGITUDE
export IMAGE_1 IMAGE_2 IMAGE_3 IMAGE_4 IMAGE_5 IMAGE_6
export RULE_1 RULE_2 RULE_3 RULE_4 RULE_5 RULE_6
export OFFSET_MIN_1 OFFSET_MIN_2 OFFSET_MIN_3 OFFSET_MIN_4 OFFSET_MIN_5 OFFSET_MIN_6
export CLOCK_TIME_1 CLOCK_TIME_2 CLOCK_TIME_3 CLOCK_TIME_4 CLOCK_TIME_5 CLOCK_TIME_6

IMG=$(/usr/bin/python3 <<'EOF'
import os
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

city = LocationInfo(
    os.environ["CITY_NAME"],
    os.environ["REGION"],
    os.environ["TIMEZONE"],
    float(os.environ["LATITUDE"]),
    float(os.environ["LONGITUDE"])
)

tz = ZoneInfo(os.environ["TIMEZONE"])
now_dt = datetime.now(tz)
s = sun(city.observer, date=now_dt.date(), tzinfo=tz)

def parse_clock_time(value: str) -> tuple[int, int]:
    hour_str, minute_str = value.split(":", 1)
    hour = int(hour_str)
    minute = int(minute_str)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError(f"Invalid clock time: {value}")
    return hour, minute


def base_time(rule: str, clock_value: str) -> datetime:
    if rule == "sunrise":
        return s["sunrise"]
    if rule == "sunset":
        return s["sunset"]
    if rule == "noon":
        return s["noon"]
    if rule == "midnight":
        return now_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if rule == "clock":
        hour, minute = parse_clock_time(clock_value)
        return now_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
    raise ValueError(f"Unsupported rule: {rule}")


slots = []
for i in range(1, 7):
    image = os.environ.get(f"IMAGE_{i}", "").strip()
    if not image:
        continue
    rule = os.environ.get(f"RULE_{i}", "clock").strip().lower()
    offset_min = int(os.environ.get(f"OFFSET_MIN_{i}", "0").strip())
    clock_value = os.environ.get(f"CLOCK_TIME_{i}", "00:00").strip()

    event_dt = base_time(rule, clock_value) + timedelta(minutes=offset_min)
    slots.append((event_dt.timestamp(), image))

if not slots:
    raise SystemExit("No image slots are configured")

slots.sort(key=lambda item: item[0])
now_ts = now_dt.timestamp()
selected = slots[-1][1]
for ts, image in slots:
    if now_ts >= ts:
        selected = image
    else:
        break

print(selected)
EOF
)

FULLPATH="$IMG"
if [[ "$FULLPATH" != /* ]]; then
    FULLPATH="$WALLDIR/$FULLPATH"
fi

if [ ! -f "$FULLPATH" ]; then
    echo "Wallpaper not found: $FULLPATH" >&2
    exit 1
fi

QDBUS=$(command -v qdbus6 || command -v qdbus)
if [ -z "$QDBUS" ]; then
    echo "qdbus command not found" >&2
    exit 1
fi

"$QDBUS" org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "
var Desktops = desktops();
for (var i = 0; i < Desktops.length; i++) {
    var d = Desktops[i];
    d.wallpaperPlugin = 'org.kde.image';
    d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');
    d.writeConfig('Image', 'file://$FULLPATH');
}
"