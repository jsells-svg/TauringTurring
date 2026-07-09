"""
Generate video from audio files using FFmpeg and PIL.
Creates scenes with text overlays for the TUZ Podcast episode.
"""

import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict
import argparse

from PIL import Image, ImageDraw, ImageFont


# ====================== CONFIGURATION ======================

CHARACTER_COLORS = {
    "Uncle Billy Bobby": {
        "bg": (25, 45, 85),        # Deep blue
        "text": (255, 200, 100),   # Warm orange
        "accent": (100, 180, 255)  # Light blue
    },
    "Jules Brunet": {
        "bg": (40, 30, 60),        # Deep purple
        "text": (200, 220, 255),   # Light blue
        "accent": (255, 150, 100)  # Warm orange
    },
    "Napoleon Bonaparte": {
        "bg": (80, 20, 20),        # Deep red
        "text": (255, 240, 200),   # Light cream
        "accent": (255, 180, 100)  # Gold
    }
}

VIDEO_SIZE = (1280, 720)
FPS = 24
CODEC = "libx264"
AUDIO_CODEC = "aac"

OUTPUT_FOLDER = "TUZ_Episode_Video"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ====================== HELPER FUNCTIONS ======================

def create_silent_audio(duration: float, output_path: Path) -> Path:
    """Create a silent WAV file using FFmpeg."""
    try:
        cmd = [
            "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
            "-t", str(duration), "-q:a", "9", "-acodec", "libmp3lame",
            str(output_path), "-y"
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to create silent audio: {e}")


def create_video_with_ffmpeg(
    concat_list: List[tuple],
    output_file: str,
    fps: int,
    codec: str,
    audio_codec: str,
    tmp_dir: Path
) -> None:
    """
    Use FFmpeg to create video from images and audio files.
    concat_list: List of (image_path, audio_path) tuples
    """
    
    # Create a temp directory for processed clips
    clips_dir = tmp_dir / "clips"
    clips_dir.mkdir(exist_ok=True)
    
    clip_paths = []
    
    for idx, (img_path, audio_path) in enumerate(concat_list):
        clip_num = idx + 1
        clip_file = clips_dir / f"clip_{clip_num:03d}.mp4"
        
        # Get audio duration
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1:nokey=1", audio_path],
                capture_output=True,
                text=True,
                check=True
            )
            duration = float(result.stdout.strip())
        except Exception:
            # If ffprobe fails, use a default
            duration = 5.0
        
        # Create clip with image looped to match audio duration
        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", img_path,
            "-i", audio_path,
            "-c:v", codec,
            "-c:a", audio_codec,
            "-shortest",
            "-r", str(fps),
            "-y",
            str(clip_file)
        ]
        
        print(f"  Creating clip {clip_num}/{len(concat_list)}...")
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            clip_paths.append(str(clip_file))
        except subprocess.CalledProcessError as e:
            print(f"    [WARNING] Failed to create clip: {e.stderr.decode()}")
            continue
    
    if not clip_paths:
        raise RuntimeError("No clips were successfully created")
    
    # Create concat demuxer file
    concat_file = tmp_dir / "concat.txt"
    with open(concat_file, "w") as f:
        for clip_path in clip_paths:
            f.write(f"file '{clip_path}'\n")
    
    # Concatenate all clips
    print(f"Concatenating {len(clip_paths)} clips into final video...")
    concat_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        "-y",
        output_file
    ]
    
    try:
        result = subprocess.run(concat_cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg concatenation failed: {e.stderr.decode()}")


# ====================== IMAGE GENERATION ======================

def create_scene_image(character: str, dialogue_preview: str, scene_num: int, size=VIDEO_SIZE) -> Image.Image:
    """Create a visual scene image for a dialogue segment."""
    
    colors = CHARACTER_COLORS.get(character, CHARACTER_COLORS["Uncle Billy Bobby"])
    bg_color = colors["bg"]
    text_color = colors["text"]
    accent_color = colors["accent"]
    
    # Create base image
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        body_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw decorative top bar
    draw.rectangle([(0, 0), (size[0], 100)], fill=accent_color, outline=accent_color)
    
    # Draw character name
    draw.text((50, 20), character.upper(), fill=bg_color, font=title_font)
    
    # Draw scene number in top right
    scene_text = f"Scene {scene_num}"
    draw.text((size[0] - 250, 30), scene_text, fill=bg_color, font=small_font)
    
    # Draw dialogue preview with text wrapping
    margin = 50
    max_width = size[0] - 2 * margin
    y_pos = 150
    
    # Wrap text to fit width
    words = dialogue_preview.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=body_font)
        line_width = bbox[2] - bbox[0]
        
        if line_width > max_width:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Draw wrapped text
    for line in lines[:5]:  # Limit to 5 lines
        draw.text((margin, y_pos), line, fill=text_color, font=body_font)
        y_pos += 80
    
    if len(lines) > 5:
        draw.text((margin, y_pos), "...", fill=text_color, font=body_font)
    
    # Draw decorative bottom bar
    draw.rectangle([(0, size[1] - 40), (size[0], size[1])], fill=accent_color, outline=accent_color)
    draw.text((50, size[1] - 30), "THE TUZ PODCAST: The Timeline Unification Zone", 
              fill=bg_color, font=small_font)
    
    return img


def create_transition_image(text: str, size=VIDEO_SIZE) -> Image.Image:
    """Create a transition/title card image."""
    
    img = Image.new("RGB", size, color=(20, 30, 50))  # Dark blue background
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw gradient effect (simple version - just colored rectangles)
    for i in range(size[1]):
        color_intensity = int(50 + (i / size[1]) * 100)
        color = (20 + color_intensity // 3, 30 + color_intensity // 3, 50 + color_intensity // 2)
        draw.line([(0, i), (size[0], i)], fill=color)
    
    # Draw title
    bbox = draw.textbbox((0, 0), text, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=(100, 180, 255), font=title_font)
    
    # Draw subtitle
    subtitle = "THE TIMELINE UNIFICATION ZONE"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = bbox[2] - bbox[0]
    x = (size[0] - sub_width) // 2
    draw.text((x, y + text_height + 30), subtitle, fill=(255, 150, 100), font=subtitle_font)
    
    return img


# ====================== VIDEO GENERATION ======================

def generate_video_from_audio(
    audio_folder: str = "TUZ_Episode_Audio",
    episode_data_file: str = None,
    output_file: str = None,
    fps: int = FPS,
    codec: str = CODEC,
    audio_codec: str = AUDIO_CODEC
) -> Path:
    """
    Generate a video from audio files with visual overlays using FFmpeg.
    
    Args:
        audio_folder: Folder containing audio files
        episode_data_file: JSON file with episode metadata
        output_file: Output video file path
        fps: Frames per second
        codec: Video codec
        audio_codec: Audio codec
    
    Returns:
        Path to generated video file
    """
    
    if episode_data_file is None:
        episode_data_file = os.path.join(audio_folder, "tuz_brunet_episode_data.json")
    
    if output_file is None:
        output_file = os.path.join(OUTPUT_FOLDER, "TUZ_Podcast_Jules_Brunet.mp4")
    
    # Load episode data
    print(f"Loading episode data from {episode_data_file}...")
    with open(episode_data_file, "r", encoding="utf-8") as f:
        episode_data = json.load(f)
    
    sections = episode_data.get("sections", [])
    if not sections:
        raise ValueError("No sections found in episode data")
    
    print(f"Found {len(sections)} sections")
    
    # Create temporary directory for images and intermediate files
    tmp_dir = Path(tempfile.mkdtemp(prefix="tuz_video_"))
    print(f"Using temp directory: {tmp_dir}")
    
    # List to track all image/audio pairs for FFmpeg concat
    concat_list = []
    
    # Add opening transition
    print("Creating opening transition...")
    opening_img = create_transition_image(f"{episode_data['episode_title']}")
    opening_path = tmp_dir / "opening.png"
    opening_img.save(opening_path)
    
    # Create 3-second silent audio for opening
    opening_audio = tmp_dir / "opening_audio.wav"
    create_silent_audio(3.0, opening_audio)
    concat_list.append((str(opening_path), str(opening_audio)))
    
    # Process each section
    for i, section in enumerate(sections, 1):
        character = section.get("character", "Unknown")
        filename = section.get("filename", "")
        dialogue_text = section.get("text", "")[:150]
        
        # Find audio file
        audio_path = os.path.join(audio_folder, filename)
        
        if not os.path.exists(audio_path):
            print(f"  [SKIP] Audio file not found: {audio_path}")
            continue
        
        print(f"Processing section {i}/{len(sections)}: {character}...")
        
        # Create scene image
        scene_img = create_scene_image(character, dialogue_text, i)
        scene_path = tmp_dir / f"scene_{i:02d}.png"
        scene_img.save(scene_path)
        
        concat_list.append((str(scene_path), audio_path))
    
    # Add closing transition
    print("Creating closing transition...")
    closing_img = create_transition_image("The Horizon Line")
    closing_path = tmp_dir / "closing.png"
    closing_img.save(closing_path)
    
    closing_audio = tmp_dir / "closing_audio.wav"
    create_silent_audio(3.0, closing_audio)
    concat_list.append((str(closing_path), str(closing_audio)))
    
    if not concat_list:
        raise RuntimeError("No content clips created for video")
    
    # Create FFmpeg concat demuxer file
    print(f"\nCombining {len(concat_list)} segments with FFmpeg...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    # Use FFmpeg to create video
    try:
        create_video_with_ffmpeg(concat_list, output_file, fps, codec, audio_codec, tmp_dir)
    except Exception as e:
        raise RuntimeError(f"Failed to create video with FFmpeg: {e}")
    
    print(f"\n[SUCCESS] Video generated: {output_file}")
    
    # Clean up temp directory
    import shutil
    shutil.rmtree(tmp_dir)
    
    return Path(output_file)


# ====================== MAIN ======================

def main():
    parser = argparse.ArgumentParser(
        description="Generate video from TUZ podcast audio files."
    )
    parser.add_argument(
        "--audio-folder",
        default="TUZ_Episode_Audio",
        help="Folder containing audio files (default: TUZ_Episode_Audio)"
    )
    parser.add_argument(
        "--episode-data",
        help="Path to episode metadata JSON file (auto-detected if not provided)"
    )
    parser.add_argument(
        "--output",
        default=os.path.join(OUTPUT_FOLDER, "TUZ_Podcast_Jules_Brunet.mp4"),
        help="Output video file path"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=FPS,
        help=f"Frames per second (default: {FPS})"
    )
    
    args = parser.parse_args()
    
    try:
        output_path = generate_video_from_audio(
            audio_folder=args.audio_folder,
            episode_data_file=args.episode_data,
            output_file=args.output,
            fps=args.fps
        )
        
        # Print file info
        if os.path.exists(output_path):
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"File size: {file_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import sys
    
    # Handle Unicode on Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    main()
