import argparse
import json
import os
import re
from datetime import datetime

# Reuse the shared ElevenLabs helper
from eleven_audio import generate_audio, combine_into_one_mp3

# ====================== CONFIGURATION ======================
UNCLE_BILLY_VOICE_ID = os.getenv("UNCLE_BILLY_VOICE_ID", "YOUR_UNCLE_BILLY_VOICE_ID")
GUEST_1_VOICE_ID = os.getenv("GUEST_1_VOICE_ID", "YOUR_GUEST_1_VOICE_ID")
GUEST_2_VOICE_ID = os.getenv("GUEST_2_VOICE_ID", "YOUR_GUEST_2_VOICE_ID")

PLACEHOLDER_VOICE_IDS = {
    "YOUR_UNCLE_BILLY_VOICE_ID",
    "YOUR_GUEST_1_VOICE_ID",
    "YOUR_GUEST_2_VOICE_ID",
}

ACTION_LINE_PATTERN = re.compile(
    r"^(?:Billy Bobby|Harriet Tubman|Winston Churchill)\s+"
    r"(?:gestures|looks|nods|turns|leans|sits|stands|walks|smiles|pauses)\b",
    re.IGNORECASE,
)

OUTPUT_FOLDER = "TUZ_Episode_Audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ====================== EPISODE DATA ======================

episode_data = {
    "episode_title": "Jules Brunet: The French Samurai",
    "series": "The TUZ Podcast (The Timeline Unification Zone)",
    "target_runtime_minutes": "12-15",
    "created": datetime.now().isoformat(),
    "tone": "Thoughtful, historical, philosophical",
    "themes": ["Honor across cultures", "Loyalty vs. orders", "Art as legacy", "Timelines and history"],
    "sections": [],
}

# ====================== PARSE SCRIPT ======================

CHARACTER_VOICE_IDS = {
    "UNCLE BILLY BOBBY": ("Uncle Billy Bobby", UNCLE_BILLY_VOICE_ID, "uncle_billy_bobby"),
    "HARRIET TUBMAN": ("Harriet Tubman", GUEST_1_VOICE_ID, "harriet_tubman"),
    "WINSTON CHURCHILL": ("Winston Churchill", GUEST_2_VOICE_ID, "winston_churchill"),
}


def parse_samplescript(script_path="samplescript.txt"):
    """
    Parse samplescript.txt and extract dialogue by character.
    Uses regex to find CHARACTER NAME followed by dialogue.
    Returns a list of dicts with character, text, and metadata.
    """
    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    parsed_sections = []
    current_character = None
    current_dialogue = []

    def flush_section():
        if current_character is None:
            return
        dialogue = "\n".join(current_dialogue).strip()
        if len(dialogue) > 10:
            parsed_sections.append((current_character, dialogue))

    for raw_line in lines:
        line = raw_line.strip()
        normalized_line = re.sub(r"^\*{1,2}|\*{1,2}$", "", line).strip()
        speaker = CHARACTER_VOICE_IDS.get(normalized_line.upper())

        if speaker:
            flush_section()
            current_character = speaker
            current_dialogue = []
            continue

        if current_character is None:
            continue
        if not line or line.startswith("(") or line.startswith("**"):
            continue
        if normalized_line.upper() in {"FADE OUT.", "SCENE END", "---"}:
            flush_section()
            current_character = None
            current_dialogue = []
            continue
        if ACTION_LINE_PATTERN.match(line):
            continue
        current_dialogue.append(line)

    flush_section()

    sections = []
    for section_id, (speaker, dialogue) in enumerate(parsed_sections, 1):
        character, voice_id, filename_stem = speaker
        sections.append({
            "id": section_id,
            "character": character,
            "section_name": f"{character} - Section {section_id}",
            "text": dialogue,
            "voice_id": voice_id,
            "filename": f"tuz_brunet_{section_id:02d}_{filename_stem}.mp3",
        })

    return sections

# ====================== MAIN EXECUTION ======================

def main(dry_run: bool = False, force: bool = False, retries: int = 3, backoff: float = 1.0):
    print("Generating TUZ Episode Audio from samplescript.txt...\n")
    episode_data["sections"] = []
    
    try:
        sections = parse_samplescript()
    except FileNotFoundError:
        print("Error: samplescript.txt not found!")
        return
    
    if not sections:
        print("Error: Could not parse any dialogue from samplescript.txt")
        return
    
    print(f"Found {len(sections)} dialogue sections\n")
    
    generated_files = []
    
    for section in sections:
        out_path = os.path.join(OUTPUT_FOLDER, section["filename"])
        
        if not section["text"]:
            print(f"[SKIP] {section['character']} - no dialogue text")
            continue
        
        print(f"[PROCESSING] {section['character']} ({len(section['text'])} chars)")
        
        if dry_run:
            # Create a small placeholder file (do not call the API)
            placeholder_path = out_path + ".dryrun.txt"
            preview = section["text"][:200].replace("\n", " ")
            with open(placeholder_path, "w", encoding="utf-8") as ph:
                ph.write(f"DRY RUN: Would generate audio for '{section['character']}'\n\n")
                ph.write(f"Text preview: {preview}...\n")
            print(f"  [DRY-RUN] would generate {out_path}")
            episode_data["sections"].append(section)
            generated_files.append(placeholder_path)
            continue
        
        # Safety gate: require explicit --force to perform live API calls
        if not force:
            raise RuntimeError("Live API calls are disabled for safety. Rerun with --force to proceed.")
        
        if section["voice_id"] in PLACEHOLDER_VOICE_IDS:
            raise RuntimeError(
                f"Voice ID for '{section['character']}' is not set. "
                "Please set the corresponding environment variable before using --force."
            )
        
        success = generate_audio(section["text"], section["voice_id"], out_path, retries=retries, backoff_factor=backoff)
        if success:
            episode_data["sections"].append(section)
            generated_files.append(out_path)
            print(f"  [SUCCESS] Generated: {out_path}")
        else:
            print(f"  [FAILED] Failed to generate audio for {section['character']}")
    
    # Save JSON data feed
    json_path = os.path.join(OUTPUT_FOLDER, "tuz_brunet_episode_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(episode_data, f, indent=2, ensure_ascii=False)
    print(f"\n[INFO] JSON data saved: {json_path}")
    
    # Optionally combine generated clips into a timestamped episode MP3
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_filename = f"TUZHorizonLine_{timestamp}.mp3"
    combined_path = os.path.join(OUTPUT_FOLDER, combined_filename)
    real_audio_files = [p for p in generated_files if p.endswith('.mp3')]
    if real_audio_files:
        try:
            combine_into_one_mp3(real_audio_files, combined_path, silence_ms=400)
            print(f"[AUDIO] Combined episode: {combined_path}")
        except Exception as e:
            print(f"[WARNING] Failed to combine files: {e}")
    
    print(f"\n[COMPLETE]")
    print(f"   Output folder: {OUTPUT_FOLDER}/")
    print(f"   Total sections: {len(episode_data['sections'])}")

if __name__ == "__main__":
    import sys
    # Handle Unicode output on Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Generate TUZ episode audio from samplescript.txt (uses ElevenLabs).")
    parser.add_argument("--dry-run", action="store_true", help="Do not call the API; write placeholders and JSON only.")
    parser.add_argument("--force", action="store_true", help="Allow live API calls (required for real generation).")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries for transient HTTP errors (default: 3)")
    parser.add_argument("--backoff", type=float, default=1.0, help="Exponential backoff base in seconds (default: 1.0)")
    args = parser.parse_args()
    main(dry_run=args.dry_run, force=args.force, retries=args.retries, backoff=args.backoff)
