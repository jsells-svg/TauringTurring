from __future__ import annotations

import tempfile
from pathlib import Path
import os
import sys
from typing import List

from PIL import Image, ImageDraw, ImageFont

from eleven_api import text_to_speech


def load_events_from_timeline(md_path: Path):
    # reuse simple parser from generate_slides.py to avoid duplication
    from generate_slides import parse_timeline

    md = md_path.read_text(encoding="utf-8")
    return parse_timeline(md)


def render_slide_image(ev: dict, out_path: Path, size=(1280, 720)):
    img = Image.new("RGB", size, color=(245, 248, 250))
    draw = ImageDraw.Draw(img)

    try:
        # try a common system font; fallback to default
        title_font = ImageFont.truetype("arial.ttf", 40)
        body_font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Title
    title = f"{ev['year']}: {ev['title']}"
    draw.text((60, 60), title, fill=(20, 40, 80), font=title_font)

    y = 140
    if ev.get("influence"):
        draw.text((80, y), f"Influence: {ev['influence']}", fill=(30, 30, 30), font=body_font)
        y += 60
    if ev.get("notes"):
        draw.text((80, y), f"Notes: {ev['notes']}", fill=(30, 30, 30), font=body_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=85)
    return out_path


def make_video(events: List[dict], out_video: Path, voice: str = "alloy", api_key: str | None = None):
    # Lazy import moviepy
    try:
        from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
    except Exception as e:
        raise RuntimeError("moviepy and ffmpeg are required to render video. Install via requirements.txt") from e

    tmp = Path(tempfile.mkdtemp(prefix="turring_video_"))
    clips = []
    for i, ev in enumerate(events, start=1):
        img_path = tmp / f"slide_{i:02d}.png"
        audio_path = tmp / f"slide_{i:02d}.wav"
        render_slide_image(ev, img_path)

        # synthesize speech using Eleven Labs
        tts_text = f"{ev['year']}. {ev['title']}. {ev.get('influence','')}. {ev.get('notes','')}"
        text_to_speech(tts_text, voice=voice, out_path=audio_path, api_key=api_key)

        audio = AudioFileClip(str(audio_path))
        img_clip = ImageClip(str(img_path)).with_duration(audio.duration).with_audio(audio)
        clips.append(img_clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(out_video), fps=24, codec="libx264", audio_codec="aac")
    return out_video


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--timeline", default="timeline.md")
    p.add_argument("--out", default="Turring_Timeline.mp4")
    p.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE", "alloy"))
    p.add_argument("--api-key", default=os.environ.get("ELEVENLABS_API_KEY"))
    args = p.parse_args()

    md_path = Path(args.timeline)
    if not md_path.exists():
        print("timeline.md not found", file=sys.stderr)
        raise SystemExit(1)

    events = load_events_from_timeline(md_path)
    print(f"Rendering {len(events)} slides to video: {args.out}")
    out_video = make_video(events, Path(args.out), voice=args.voice, api_key=args.api_key)
    print("Wrote", out_video)


if __name__ == "__main__":
    main()
