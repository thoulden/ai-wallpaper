#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="$(which python3)"

# Remove any existing wallpaper job, then add a fresh weekly one (Monday 9 AM)
( crontab -l 2>/dev/null | grep -v "$SCRIPT_DIR/wallpaper.py"
  echo "0 9 * * 1 cd \"$SCRIPT_DIR\" && $PYTHON_BIN wallpaper.py >> \"$SCRIPT_DIR/wallpaper.log\" 2>&1"
) | crontab -

echo "✅ Wallpaper automation started! (Runs weekly on Mondays at 9 AM)"
echo "📝 Output will be logged to: $SCRIPT_DIR/wallpaper.log"
echo "Run ./stop_wallpaper_schedule.sh to stop"
