import os
import sys
import requests
from pydub import AudioSegment

# ====================== CONFIG ======================
# Provide your ElevenLabs API key via the environment variable
# `ELEVENLABS_API_KEY` or `XI_API_KEY`.
API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("XI_API_KEY")

if not API_KEY:
    # don't exit immediately when imported — only when run as script
    pass

# ====================== FUNCTIONS ======================

def generate_audio(text, voice_id, filename):
    """Generate an MP3 from `text` using ElevenLabs voice `voice_id`.

    Saves output to `filename`.
    """
    if not API_KEY:
        raise RuntimeError("ELEVENLABS API key not set in ELEVENLABS_API_KEY or XI_API_KEY")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY,
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.78,
            "similarity_boost": 0.85,
            "style": 0.55,
            "use_speaker_boost": True,
        },
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
    except Exception as e:
        print(f"❌ Error requesting TTS: {e}")
        return False

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Generated: {filename}")
        return True
    else:
        # Show response body for debugging when available
        body = response.text[:400]
        print(f"❌ Error generating {filename}: {response.status_code} - {body}")
        return False


def combine_into_one_mp3(file_list, output_filename, silence_ms=300):
    """Combines multiple MP3s into one file with short pauses between clips.

    `file_list` should be a list of file paths to MP3 files.
    """
    combined = AudioSegment.empty()

    for i, file in enumerate(file_list):
        audio = AudioSegment.from_mp3(file)
        combined += audio

        # Add a short silence after each clip except the last
        if i < len(file_list) - 1:
            combined += AudioSegment.silent(duration=silence_ms)

    combined.export(output_filename, format="mp3")
    print(f"🎉 Successfully created combined file: {output_filename}")
    print(f" Total length: {len(combined) / 1000:.1f} seconds")


# ====================== MAIN EXECUTION ======================

def _example_main():
    """Example runner. Replace the placeholder texts and voice IDs before use."""
    if not API_KEY:
        print("ELEVENLABS API key not found. Please set ELEVENLABS_API_KEY or XI_API_KEY.")
        sys.exit(1)

    # Placeholder texts — replace these with your real content
    uncle_opening = (
        "[Replace this text] Uncle Billy opens the episode with a short intro."
    )
    crazy_horse = "[Replace this text] Crazy Horse speaks about the plains."
    shaka_zulu = "[Replace this text] Shaka Zulu recounts a battle."
    uncle_closing = "[Replace this text] Uncle Billy closes the episode."

    # Voice IDs — set real voice IDs as env vars or replace these strings
    UNCLE_BILLY_VOICE_ID = os.getenv("UNCLE_BILLY_VOICE_ID", "your_uncle_billy_voice_id")
    CRAZY_HORSE_VOICE_ID = os.getenv("CRAZY_HORSE_VOICE_ID", "your_crazy_horse_voice_id")
    SHAKA_ZULU_VOICE_ID = os.getenv("SHAKA_ZULU_VOICE_ID", "your_shaka_zulu_voice_id")

    print("Generating individual voice clips...\n")

    generate_audio(uncle_opening, UNCLE_BILLY_VOICE_ID, "01_uncle_opening.mp3")
    generate_audio(crazy_horse, CRAZY_HORSE_VOICE_ID, "02_crazy_horse.mp3")
    generate_audio(shaka_zulu, SHAKA_ZULU_VOICE_ID, "03_shaka_zulu.mp3")
    generate_audio(uncle_closing, UNCLE_BILLY_VOICE_ID, "04_uncle_closing.mp3")

    print("\nCombining all clips into one podcast episode...")

    files_in_order = [
        "01_uncle_opening.mp3",
        "02_crazy_horse.mp3",
        "03_shaka_zulu.mp3",
        "04_uncle_closing.mp3",
    ]

    combine_into_one_mp3(files_in_order, "TUZ_Podcast_Landscapes_We_Loved.mp3", silence_ms=400)

    print("\n✅ Done.")


if __name__ == "__main__":
    _example_main()
