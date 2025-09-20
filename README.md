# AI Wallpaper Generator

Automatically generate and set unique AI-created wallpapers for your Mac using OpenAI's image generation API, with subtle continuity between generations.

## Features

- Generates cinematic, background-friendly images (wide composition, detailed yet calm)
- Prompts evolve over time based on the previous prompt
- Fully automated via cron (weekly by default; minute-based test mode included)
- Logs all runs to `wallpaper.log` for easy debugging
- Saves images to `~/Pictures/AI_Wallpapers/` and (optionally) cleans older ones

---

## Quick Start Setup (Mac)

Follow these steps to get running end-to-end.

1) Clone or download the project
~~~~bash
git clone https://github.com/your-username/ai-wallpaper.git
cd ai-wallpaper
~~~~

2) Install required Python packages
~~~~bash
pip install openai requests python-dotenv
~~~~

3) Create your `.env` file with your OpenAI API key
~~~~bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
~~~~

4) Make helper scripts executable
~~~~bash
chmod +x start_wallpaper_schedule.sh start_wallpaper_schedule_test.sh stop_wallpaper_schedule.sh check_wallpaper_schedule.sh
~~~~

5) Grant macOS permissions (important for scheduled runs)

- Open **System Settings → Privacy & Security → Full Disk Access**
- Add and enable:
  - Your Python binary (find it with `which python3`)
  - `cron` at `/usr/sbin/cron`
  - Optional but helpful: `/bin/bash` and `/usr/bin/osascript`
- Then restart cron so changes take effect:
~~~~bash
sudo launchctl kickstart -k system/com.vix.cron
~~~~

6) Test a manual run
~~~~bash
python3 wallpaper.py
~~~~
This should create a new image under `~/Pictures/AI_Wallpapers/` and set it as the desktop wallpaper (macOS).

7) Test the automation (minute-by-minute)
~~~~bash
./start_wallpaper_schedule_test.sh
tail -f wallpaper.log
~~~~
Stop the test when finished:
~~~~bash
./stop_wallpaper_schedule.sh
~~~~

8) Enable the weekly schedule (Mondays at 09:00)
~~~~bash
./start_wallpaper_schedule.sh
~~~~

---

## Project Files

- `wallpaper.py` — Main runner. Generates a prompt, calls the OpenAI image API, saves the image in `~/Pictures/AI_Wallpapers/`, sets it as wallpaper on macOS, and logs to `wallpaper.log`.
- `prompt_gen.py` — GPT-powered prompt scaffolding. Produces concise, cinematic prompts and persists continuity between runs.
- `last_prompt_state.json` — Machine-readable state storing the last prompt for continuity (auto-created).
- `last_prompt.txt` — Human-readable copy of the last prompt (auto-created).
- `wallpaper.log` — Log file (auto-populated by scheduled runs).
- `start_wallpaper_schedule.sh` — Installs a weekly cron job (Monday 09:00) that logs to `wallpaper.log`.
- `start_wallpaper_schedule_test.sh` — Installs a per-minute cron job for testing (also logs to `wallpaper.log`).
- `stop_wallpaper_schedule.sh` — Removes any cron lines containing `wallpaper.py`.
- `check_wallpaper_schedule.sh` — Shows whether a wallpaper cron entry is active.

---

## Automation

Start weekly schedule
~~~~bash
./start_wallpaper_schedule.sh
~~~~

Start per-minute test schedule
~~~~bash
./start_wallpaper_schedule_test.sh
tail -f wallpaper.log
~~~~

Check if a wallpaper job is active
~~~~bash
./check_wallpaper_schedule.sh
# or
crontab -l
~~~~

Stop all wallpaper cron jobs
~~~~bash
./stop_wallpaper_schedule.sh
~~~~

---

## Customization

Change the schedule  
Edit `start_wallpaper_schedule.sh` and modify the cron expression:
- `0 9 * * 1` — Mondays at 09:00 (default)
- `0 9 * * *` — Daily at 09:00
- `*/30 * * * *` — Every 30 minutes

Tweak prompt behavior  
Edit `prompt_gen.py` to adjust the system instructions or model used for generating prompts.

Keep all wallpapers  
In `wallpaper.py`, comment out the cleanup section if you want to keep every generated image.

Rotate logs (optional)  
Add a weekly log reset alongside your existing cron entries:
~~~~bash
( crontab -l 2>/dev/null; echo "0 0 * * 0 > $(pwd)/wallpaper.log" ) | crontab -
~~~~

---

## Troubleshooting

View logs
~~~~bash
tail -n 100 wallpaper.log
~~~~

See installed cron jobs
~~~~bash
crontab -l
~~~~

Manual wallpaper set test (bypasses Python)
~~~~bash
osascript -e 'tell application "System Events" to set picture of every desktop to POSIX file "'"$HOME/Pictures/AI_Wallpapers/any.png"'"'
~~~~

If scheduled runs do nothing
- Re-check Full Disk Access: make sure both your `python3` path and `/usr/sbin/cron` are allowed
- Restart cron again:
~~~~bash
sudo launchctl kickstart -k system/com.vix.cron
~~~~

Remove all cron jobs (nuclear option)
~~~~bash
crontab -r
~~~~

---

## API Usage and Costs

- Each run performs one image-generation API call
- Weekly schedule is roughly four images per month
- Check current pricing and usage in your OpenAI account dashboard
- Store your `.env` locally and never commit it to version control

---

## Privacy

- The API key is stored locally in `.env`
- Images and logs are stored locally on your machine
- Data is sent only to OpenAI for image generation
