import os
import sys
from datetime import datetime
import subprocess
import platform

# Add the script's directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from prompt_gen import generate_prompt, save_prompt, load_last_prompt
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Folder for wallpapers - using absolute path
WALLPAPER_DIR = os.path.expanduser("~/Pictures/AI_Wallpapers")
os.makedirs(WALLPAPER_DIR, exist_ok=True)

print(f"📁 Wallpaper directory: {WALLPAPER_DIR}")
print(f"📁 Directory exists: {os.path.exists(WALLPAPER_DIR)}")

# Clean up old wallpapers
old_files = os.listdir(WALLPAPER_DIR)
if old_files:
    print(f"🗑️  Cleaning up {len(old_files)} old wallpaper(s)...")
    for file in old_files:
        if file.endswith(('.png', '.jpg', '.jpeg')):
            os.remove(os.path.join(WALLPAPER_DIR, file))

# Generate new prompt (but don't save it yet)
last_prompt = load_last_prompt()
prompt = generate_prompt(last_prompt)
print(f"🎨 Generated prompt: {prompt[:100]}...")

# Generate image
print("🖼️  Requesting image from OpenAI...")
try:
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="low"
    )
    
    # DEBUG info
    print(f"📋 Response type: {type(result)}")
    print(f"📋 Response data attribute exists: {hasattr(result, 'data')}")
    if hasattr(result, 'data'):
        print(f"📋 Response data: {result.data}")
        if result.data:
            print(f"📋 Number of items in data: {len(result.data)}")
    
    # Try to get the image URL or base64 data
    image_url = None
    image_b64 = None
    
    if result and result.data and len(result.data) > 0:
        if hasattr(result.data[0], 'url') and result.data[0].url:
            image_url = result.data[0].url
            print(f"✅ Got image URL")
        elif hasattr(result.data[0], 'b64_json') and result.data[0].b64_json:
            image_b64 = result.data[0].b64_json
            print(f"✅ Got base64 image data")
    
    if not image_url and not image_b64:
        print(f"❌ No image URL or base64 data in response")
        print(f"Full response object: {vars(result) if hasattr(result, '__dict__') else result}")
        exit(1)
    
    # Handle URL-based image
    if image_url:
        print("📥 Downloading image from URL...")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image_data = response.content
        print(f"✅ Downloaded {len(image_data):,} bytes")
    
    # Handle base64-based image
    elif image_b64:
        print("📥 Decoding base64 image...")
        import base64
        image_data = base64.b64decode(image_b64)
        print(f"✅ Decoded {len(image_data):,} bytes")
    
    # Save image
    filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(WALLPAPER_DIR, filename)
    
    with open(path, "wb") as f:
        bytes_written = f.write(image_data)
    
    # Verify the file was saved
    if os.path.exists(path):
        file_size = os.path.getsize(path)
        print(f"✅ Wallpaper saved: {path}")
        print(f"✅ File size: {file_size:,} bytes")

        # ✅ Save the prompt only after we know the wallpaper was successfully saved
        save_prompt(prompt)
        print(f"📝 Prompt saved to last_prompt.txt")

        # Automatically set as wallpaper on macOS
        if platform.system() == 'Darwin':
            print("🖼  Updating macOS wallpaper...")
            subprocess.run([
                "osascript", "-e",
                f'tell application "System Events" to set picture of every desktop to POSIX file "{path}"'
            ])
            print("✅ Wallpaper updated on macOS")
        elif platform.system() == 'Windows':
            print("ℹ️ Wallpaper update automation not implemented for Windows yet.")
            
    else:
        print(f"❌ File was not saved properly at {path}")
        
except requests.RequestException as e:
    print(f"❌ Network error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
