from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import textwrap
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image, ImageDraw, ImageFont

from eleven_api import text_to_speech

SCENE_HEADING_RE = re.compile(r"^(INT|EXT|INT/EXT|EXT/INT)\b.*", re.IGNORECASE)
SPEAKER_COLON_RE = re.compile(r"^([A-Z0-9 ]{2,50}):\s*(.*)$")


def normalize_character(name: str) -> str:
    return name.strip().upper()


def parse_screenplay(screenplay_text: str) -> List[Dict[str, str]]:
    lines = [line.rstrip() for line in screenplay_text.splitlines()]
    blocks: List[Dict[str, str]] = []
    current_speaker: Optional[str] = None
    current_text: List[str] = []

    def flush_dialogue() -> None:
        nonlocal current_speaker, current_text
        if current_speaker and current_text:
            blocks.append(
                {
                    "type": "dialogue",
                    "speaker": current_speaker,
                    "text": " ".join(current_text).strip(),
                }
            )
        current_speaker = None
        current_text = []

    def flush_action() -> None:
        nonlocal current_text
        if current_text:
            blocks.append(
                {
                    "type": "action",
                    "text": " ".join(current_text).strip(),
                }
            )
        current_text = []

    for raw in lines + [""]:
        line = raw.strip()
        if not line:
            if current_speaker:
                flush_dialogue()
            else:
                flush_action()
            current_speaker = None
            current_text = []
            continue

        if SCENE_HEADING_RE.match(line):
            if current_speaker:
                flush_dialogue()
            elif current_text:
                flush_action()
            blocks.append({"type": "scene", "text": line})
            continue

        speaker_match = SPEAKER_COLON_RE.match(line)
        if speaker_match:
            if current_speaker:
                flush_dialogue()
            elif current_text:
                flush_action()
            current_speaker = normalize_character(speaker_match.group(1))
            current_text = [speaker_match.group(2)] if speaker_match.group(2) else []
            continue

        if line == line.upper() and len(line) <= 50 and not re.search(r"[.!?]", line):
            if current_speaker:
                flush_dialogue()
            elif current_text:
                flush_action()
            current_speaker = normalize_character(line)
            current_text = []
            continue

        current_text.append(line)

    return blocks


def build_tts_text(block: Dict[str, str]) -> str:
    if block["type"] == "scene":
        return f"Scene heading: {block['text']}."
    if block["type"] == "dialogue":
        speaker = block.get("speaker", "Narrator")
        return f"{speaker} says: {block['text']}"
    return f"Stage direction: {block['text']}"


def render_slide_image(block: Dict[str, str], out_path: Path, size=(1280, 720)) -> Path:
    img = Image.new("RGB", size, color=(30, 34, 38))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 44)
        body_font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    title = ""
    subtitle = ""
    if block["type"] == "scene":
        title = block["text"]
        subtitle = "Scene heading"
    elif block["type"] == "dialogue":
        title = block.get("speaker", "Unknown")
        subtitle = block["text"]
    else:
        title = "Stage Direction"
        subtitle = block["text"]

    draw.text((60, 60), title, fill=(255, 255, 255), font=title_font)
    if subtitle:
        wrapped = textwrap.wrap(subtitle, width=50)
        y = 140
        for line in wrapped:
            draw.text((70, y), line, fill=(220, 220, 220), font=body_font)
            line_bbox = draw.textbbox((70, y), line, font=body_font)
            y += line_bbox[3] - line_bbox[1] + 10

    footer = "Generated from screenplay input"
    draw.text((60, size[1] - 70), footer, fill=(140, 140, 160), font=body_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=90)
    return out_path


def load_voice_map(path: Optional[Path]) -> Dict[str, str]:
    if path is None:
        return {}
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    voices = data.get("voices") if isinstance(data, dict) else None
    if not isinstance(voices, dict):
        raise ValueError("Voice map file must contain a top-level 'voices' object.")
    return {normalize_character(k): v for k, v in voices.items()}


def make_video(
    screenplay_path: Path,
    out_video: Path,
    voice: str = "alloy",
    api_key: Optional[str] = None,
    voice_map_path: Optional[Path] = None,
) -> Path:
    try:
        from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
    except Exception as exc:
        raise RuntimeError(
            "moviepy and ffmpeg are required to render video. Install via requirements.txt"
        ) from exc

    raw_text = screenplay_path.read_text(encoding="utf-8")
    blocks = parse_screenplay(raw_text)
    if not blocks:
        raise RuntimeError("No screenplay blocks were parsed from the input file.")

    voice_map = load_voice_map(voice_map_path)
    tmp_dir = Path(tempfile.mkdtemp(prefix="screenplay_video_"))
    clips = []

    for index, block in enumerate(blocks, start=1):
        image_path = tmp_dir / f"slide_{index:03d}.png"
        audio_path = tmp_dir / f"slide_{index:03d}.mp3"
        render_slide_image(block, image_path)

        line_voice = voice
        if block["type"] == "dialogue":
            speaker_key = normalize_character(block.get("speaker", ""))
            line_voice = voice_map.get(speaker_key, voice)

        tts_text = build_tts_text(block)
        generated_audio_path = text_to_speech(tts_text, voice=line_voice, out_path=audio_path, api_key=api_key)

        audio_clip = AudioFileClip(str(generated_audio_path))
        clip = ImageClip(str(image_path)).set_duration(audio_clip.duration).set_audio(audio_clip)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(out_video), fps=24, codec="libx264", audio_codec="aac")
    return out_video


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a video from a screenplay text file using Eleven Labs speech synthesis."
    )
    parser.add_argument("--screenplay", required=True, help="Path to a screenplay text file.")
    parser.add_argument("--out", default="screenplay_video.mp4", help="Output video path.")
    parser.add_argument(
        "--voice",
        default=os.environ.get("ELEVENLABS_VOICE", "alloy"),
        help="Default Eleven Labs voice id or name.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ELEVENLABS_API_KEY"),
        help="Eleven Labs API key. If omitted, read from ELEVENLABS_API_KEY env var.",
    )
    parser.add_argument(
        "--voice-map",
        default=None,
        help="Optional JSON file with a voices mapping for character names.",
    )
    args = parser.parse_args()

    screenplay_path = Path(args.screenplay)
    if not screenplay_path.exists():
        raise SystemExit(f"Screenplay file not found: {screenplay_path}")

    voice_map_path = Path(args.voice_map) if args.voice_map else None
    out_video = Path(args.out)
    result = make_video(
        screenplay_path,
        out_video,
        voice=args.voice,
        api_key=args.api_key,
        voice_map_path=voice_map_path,
    )
    print(f"Wrote video: {result}")


if __name__ == "__main__":
    main()
