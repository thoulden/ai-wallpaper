cat > stop_wallpaper_schedule.sh << 'EOF'
#!/bin/bash

# Remove the wallpaper line from crontab
crontab -l | grep -v 'wallpaper.py' | crontab -

echo "🛑 Wallpaper automation stopped!"
EOF