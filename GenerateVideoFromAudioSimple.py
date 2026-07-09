"""
Generate video from audio files using imageio and PIL.
Creates scenes with text overlays for the TUZ Podcast episode.
"""

import os
import json
import tempfile
from pathlib import Path
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont
import numpy as np

try:
    import imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    IMAGEIO_AVAILABLE = False


# ====================== CONFIGURATION ======================

CHARACTER_COLORS = {
    "Uncle Billy Bobby": {
        "bg": (25, 45, 85),
        "text": (255, 200, 100),
        "accent": (100, 180, 255)
    },
    "Jules Brunet": {
        "bg": (40, 30, 60),
        "text": (200, 220, 255),
        "accent": (255, 150, 100)
    },
    "Napoleon Bonaparte": {
        "bg": (80, 20, 20),
        "text": (255, 240, 200),
        "accent": (255, 180, 100)
    }
}

VIDEO_SIZE = (1280, 720)
FPS = 24

OUTPUT_FOLDER = "TUZ_Episode_Video"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


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

def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds using a simple method."""
    try:
        # Try to read audio file properties
        if audio_path.endswith('.mp3'):
            # For MP3 files, try to estimate from file size
            # Average MP3 bitrate: 128 kbps = 16 KB/s
            file_size = os.path.getsize(audio_path)
            estimated_duration = file_size / 16000  # bytes to seconds
            return max(1.0, estimated_duration)  # At least 1 second
        else:
            # Try imageio audio reading
            try:
                audio = imageio.get_reader(audio_path)
                return len(audio) / audio.get_meta_data().get('fps', 44100)
            except:
                return 5.0  # Default fallback
    except Exception as e:
        print(f"    [WARNING] Could not determine duration for {audio_path}: {e}")
        return 5.0


def generate_video_from_audio(
    audio_folder: str = "TUZ_Episode_Audio",
    episode_data_file: str = None,
    output_file: str = None,
    fps: int = FPS
) -> Path:
    """
    Generate a video from audio files with visual overlays using imageio.
    
    Args:
        audio_folder: Folder containing audio files
        episode_data_file: JSON file with episode metadata
        output_file: Output video file path
        fps: Frames per second
    
    Returns:
        Path to generated video file
    """
    
    if not IMAGEIO_AVAILABLE:
        raise RuntimeError("imageio is required for video generation")
    
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
    
    # Create temporary directory for images
    tmp_dir = Path(tempfile.mkdtemp(prefix="tuz_video_"))
    print(f"Using temp directory: {tmp_dir}")
    
    # Video frames list
    all_frames = []
    all_audio = []
    
    # Add opening transition
    print("Creating opening transition...")
    opening_img = create_transition_image(f"{episode_data['episode_title']}")
    opening_path = tmp_dir / "opening.png"
    opening_img.save(opening_path)
    
    # Convert PIL image to numpy array for frame repetition
    opening_array = np.array(opening_img)
    opening_frames = [opening_array] * (int(3 * fps))  # 3 seconds
    all_frames.extend(opening_frames)
    
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
        
        # Get audio duration
        duration = get_audio_duration(audio_path)
        num_frames = int(duration * fps)
        
        # Convert image to numpy array and repeat for duration
        scene_array = np.array(scene_img)
        scene_frames = [scene_array] * num_frames
        all_frames.extend(scene_frames)
        
        print(f"  Added {num_frames} frames ({duration:.1f}s)")
    
    # Add closing transition
    print("Creating closing transition...")
    closing_img = create_transition_image("The Horizon Line")
    closing_path = tmp_dir / "closing.png"
    closing_img.save(closing_path)
    
    closing_array = np.array(closing_img)
    closing_frames = [closing_array] * (int(3 * fps))  # 3 seconds
    all_frames.extend(closing_frames)
    
    if not all_frames:
        raise RuntimeError("No frames created for video")
    
    print(f"\nTotal frames: {len(all_frames)}")
    print(f"Video duration: {len(all_frames) / fps:.1f} seconds")
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    # Write video
    print(f"Writing video to {output_file}...")
    try:
        writer = imageio.get_writer(output_file, fps=fps, codec='libx264')
        for frame in all_frames:
            writer.append_data(frame)
        writer.close()
        print(f"[SUCCESS] Video generated: {output_file}")
    except Exception as e:
        raise RuntimeError(f"Failed to write video: {e}")
    
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
    main()
