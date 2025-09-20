#!/bin/bash

# Check if wallpaper script is scheduled
if crontab -l 2>/dev/null | grep -q 'wallpaper.py'; then
    echo "✅ Wallpaper automation is ACTIVE"
    echo "Current schedule:"
    crontab -l | grep 'wallpaper.py'
else
    echo "🔴 Wallpaper automation is NOT active"
fi
