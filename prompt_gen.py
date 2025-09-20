import os
import json
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

STATE_FILE = "last_prompt_state.json"
PROMPT_FILE = "last_prompt.txt"

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _load_state() -> Optional[dict]:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def _save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def generate_prompt(last_prompt: Optional[str] = None) -> str:
    """
    Ask GPT to generate a new beautiful, cinematic, background-friendly image prompt,
    with subtle continuity from the last prompt.
    """
    system_msg = (
        "You are a creative assistant generating prompts for AI image generation. "
        "Your goal is to create a series of weekly wallpapers that are beautiful, cinematic, "
        "and suitable as desktop backgrounds. Each prompt should:\n"
        "- Be a single descriptive sentence or two.\n"
        "- Contain a clear subject or scene, a mood, and stylistic details.\n"
        "- Be visually striking but not too busy.\n"
        "- Use descriptive words like 'cinematic wide shot', 'high resolution', "
        "'painterly softness', 'photorealistic detail', etc.\n"
        "- Evolve subtly from the previous prompt (if provided) by developing the same scene, "
        "shifting the mood, or introducing a new element."
    )

    user_msg = "Generate the next prompt in this evolving wallpaper series."
    if last_prompt:
        user_msg += f"\nPrevious prompt:\n{last_prompt}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Small, cheap model for prompt generation
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=150,
    )

    new_prompt = response.choices[0].message.content.strip()

    # Save prompt + state for next time
    save_prompt(new_prompt)
    _save_state({"last_prompt": new_prompt})

    return new_prompt

def save_prompt(prompt: str, filepath=PROMPT_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(prompt)

def load_last_prompt(filepath=PROMPT_FILE) -> Optional[str]:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

if __name__ == "__main__":
    try:
        print("→ Running prompt_gen.py")
        lp = load_last_prompt()
        print("Last prompt:", lp)
        new_prompt = generate_prompt(lp)
        print("New prompt:", new_prompt)
    except Exception as e:
        import traceback
        print("❌ Error while generating prompt:", e)
        traceback.print_exc()