import os
import requests
from pathlib import Path

ELEVEN_API_BASE = "https://api.elevenlabs.io/v1"


def text_to_speech(text: str, voice: str, out_path: str | Path, api_key: str | None = None, model: str = "eleven_multilingual_v1"):
    """Synthesize speech via Eleven Labs Text-to-Speech API, with a local fallback.

    Args:
        text: Text to synthesize.
        voice: Voice id or name. Example: 'alloy' or a voice UUID.
        out_path: File path to write audio.
        api_key: Eleven Labs API key. If None, reads from ELEVENLABS_API_KEY env var.
        model: Optional model name.

    Returns: Path to written audio file.
    """
    out_path = Path(out_path)

    if api_key is None:
        api_key = os.environ.get("ELEVENLABS_API_KEY")

    if api_key:
        try:
            url = f"{ELEVEN_API_BASE}/text-to-speech/{voice}"
            headers = {
                "xi-api-key": api_key,
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
            }
            payload = {"text": text, "model": model}

            resp = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
            resp.raise_for_status()

            with out_path.open("wb") as fh:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        fh.write(chunk)
            return out_path
        except Exception:
            # Fall back to local speech synthesis below.
            pass

    try:
        import pyttsx3
    except ImportError as exc:
        raise RuntimeError("No Eleven Labs key and pyttsx3 is not available. Install pyttsx3 or provide ELEVENLABS_API_KEY") from exc

    # pyttsx3 saves WAV files; use the same path if it already ends in .wav, otherwise derive a .wav name.
    wav_path = out_path if out_path.suffix.lower() == ".wav" else out_path.with_suffix(".wav")
    engine = pyttsx3.init()
    engine.save_to_file(text, str(wav_path))
    engine.runAndWait()
    return wav_path


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True)
    p.add_argument("--voice", default="alloy")
    p.add_argument("--out", default="out.mp3")
    p.add_argument("--api-key", default=None)
    args = p.parse_args()
    path = text_to_speech(args.text, args.voice, args.out, api_key=args.api_key)
    print("Wrote", path)
