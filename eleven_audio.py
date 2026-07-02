import os
import shutil
import subprocess
import tempfile
import sys
import time

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

# ====================== CONFIG ======================
# Provide your ElevenLabs API key via the environment variable
# `ELEVENLABS_API_KEY` or `XI_API_KEY`.
#
# Also configure voice IDs for each speaker in the example runner via
# `UNCLE_BILLY_VOICE_ID`, `CRAZY_HORSE_VOICE_ID`, and `SHAKA_ZULU_VOICE_ID`.
def get_api_key():
    return os.getenv("ELEVENLABS_API_KEY") or os.getenv("XI_API_KEY")

# ====================== FUNCTIONS ======================

def generate_audio(text, voice_id, filename, retries: int = 3, backoff_factor: float = 1.0):
    """Generate an MP3 from `text` using ElevenLabs voice `voice_id`.

    Retries on transient errors (429, 5xx). Saves output to `filename`.
    """
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("ELEVENLABS API key not set in ELEVENLABS_API_KEY or XI_API_KEY")

    import requests

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
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

    attempt = 1
    while attempt <= max(1, retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
        except Exception as e:
            if attempt < retries:
                wait = backoff_factor * (2 ** (attempt - 1))
                print(f"⚠️ Request error (attempt {attempt}/{retries}): {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
                attempt += 1
                continue
            else:
                print(f"❌ Error requesting TTS after {attempt} attempts: {e}")
                return False

        status = response.status_code
        if status == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Generated: {filename}")
            return True

        # Retry on rate limit or server errors
        if status == 429 or 500 <= status < 600:
            if attempt < retries:
                wait = backoff_factor * (2 ** (attempt - 1))
                body = response.text[:300]
                print(f"⚠️ Transient HTTP {status} (attempt {attempt}/{retries}): {body}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
                attempt += 1
                continue
            else:
                body = response.text[:800]
                print(f"❌ Error generating {filename}: HTTP {status} - {body}")
                return False

        # Permanent client error
        body = response.text[:800]
        print(f"❌ Error generating {filename}: HTTP {status} - {body}")
        return False


def _join_mp3_with_ffmpeg(file_list, output_filename):
    """Concatenate MP3 files using ffmpeg if pydub is unavailable."""
    # ffmpeg-python may not be installed or may not see a working binary.
    # Use imageio_ffmpeg binary if available, or fallback to system ffmpeg.
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path or not os.path.isfile(ffmpeg_path):
        raise RuntimeError(
            "ffmpeg is required for MP3 combination. Install ffmpeg or configure imageio-ffmpeg."
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        list_path = os.path.join(tmpdir, "inputs.txt")
        with open(list_path, "w", encoding="utf-8") as f:
            for file in file_list:
                path = os.path.abspath(file)
                path = path.replace("'", "'\\''")
                f.write(f"file '{path}'\n")

        cmd = [
            ffmpeg_path,
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_path,
            "-c",
            "copy",
            output_filename,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg concat failed: {result.returncode}\n{result.stderr.strip()}"
            )

    print(f"Successfully created combined file: {output_filename}")


def combine_into_one_mp3(file_list, output_filename, silence_ms=300):
    """Combines multiple MP3s into one file with short pauses between clips.

    `file_list` should be a list of file paths to MP3 files.
    """
    if AudioSegment is not None:
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
        return

    # Fallback: try ffmpeg concat if pydub is unavailable
    print("pydub not available; falling back to ffmpeg concat.")
    _join_mp3_with_ffmpeg(file_list, output_filename)


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
