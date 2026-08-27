import argparse
import json
import os
from datetime import datetime

# Reuse the shared ElevenLabs helper
from eleven_audio import generate_audio, combine_into_one_mp3

# ====================== CONFIGURATION ======================
# The ElevenLabs API key is read by `eleven_audio` from the
# environment variable `ELEVENLABS_API_KEY` or `XI_API_KEY`.

# Voice IDs: prefer environment variables, fall back to placeholder strings
UNCLE_BILLY_VOICE_ID = os.getenv("UNCLE_BILLY_VOICE_ID", "YOUR_UNCLE_BILLY_VOICE_ID")
CRAZY_HORSE_VOICE_ID = os.getenv("CRAZY_HORSE_VOICE_ID", "YOUR_CRAZY_HORSE_VOICE_ID")
SHAKA_ZULU_VOICE_ID  = os.getenv("SHAKA_ZULU_VOICE_ID", "YOUR_SHAKA_ZULU_VOICE_ID")
CUSTER_VOICE_ID      = os.getenv("CUSTER_VOICE_ID", "YOUR_CUSTER_VOICE_ID")

PLACEHOLDER_VOICE_IDS = {
    "YOUR_UNCLE_BILLY_VOICE_ID",
    "YOUR_CRAZY_HORSE_VOICE_ID",
    "YOUR_SHAKA_ZULU_VOICE_ID",
    "YOUR_CUSTER_VOICE_ID",
}

OUTPUT_FOLDER = "TUZ_Episode_Audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ====================== EPISODE DATA ======================

episode_data = {
    "episode_title": "The Landscapes We Loved",
    "series": "The TUZ Podcast (The Understanding Zone)",
    "target_runtime_minutes": "8.5-9.5",
    "created": datetime.now().isoformat(),
    "tone": "Warm, respectful, healing-focused for ages 11-12",
    "includes_senate_resolution": "S.Res.795 (119th Congress) - 150th anniversary of the Battle of the Little Bighorn",
    "sections": [],
    "primary_sources": [
        {
            "title": "Fort Laramie Treaty of 1868",
            "link": "https://www.archives.gov/milestone-documents/fort-laramie-treaty",
            "description": "The actual treaty document about the Black Hills"
        },
        {
            "title": "Letters by General Custer",
            "link": "https://www.rochestervoices.org/collections/george-a-custer-letters/",
            "description": "Original letters written by Custer"
        },
        {
            "title": "S.Res.795 - 150th Anniversary Resolution",
            "link": "https://congress.gov/bill/119-congress/senate-resolution/795",
            "description": "U.S. Senate resolution commemorating the 150th anniversary of the Battle of the Little Bighorn (passed June 2026)"
        },
        {
            "title": "Understanding Primary Sources",
            "link": "https://www.loc.gov/programs/teachers/getting-started-with-primary-sources/",
            "description": "Library of Congress guide for students"
        }
    ]
}

# ====================== TEXT SECTIONS ======================

sections = [
    {
        "id": 1,
        "character": "Uncle Billy Bobby",
        "section_name": "Opening & Introduction",
        "text": """Hello everyone, and welcome back to The TUZ Podcast — The Understanding Zone. I’m Uncle Billy Bobby.

Today we’re going on a special journey. We’re going to hear from three very different people about the lands they loved — the places they called home.

Before we talk about battles, I want you kids listening to understand something important: You can’t understand why someone fights unless you understand what they were fighting for.

So today, we’re going to close our eyes and picture the landscapes these warriors came from.

Crazy Horse, when you think about the Black Hills — the land you and your people fought so hard to protect — what do you see?""",
        "voice_id": UNCLE_BILLY_VOICE_ID,
        "visual_cue": "Start with Campfire Gathering Scene - wide shot of all characters",
        "filename": "01_uncle_opening.mp3"
    },
    {
        "id": 2,
        "character": "Crazy Horse",
        "section_name": "Black Hills Description",
        "text": """I see pine trees growing so thick and dark that when you look at the mountains from far away, they almost look black. That is why we call them Paha Sapa — the Black Hills.

I remember the smell of damp earth after rain, the sharp scent of fresh pine needles, and the sound of clear mountain rivers rushing over rocks.

To the Lakota people, these hills were not just beautiful. They were sacred. This was the place where we went to pray and have visions. It was where the animals lived that gave us food and clothing. It was where our ancestors were buried.

Looking out at those mountains felt like looking at the face of someone you love deeply. When someone tries to take that away, it is not just land they are taking — it is part of your heart and your people’s story.""",
        "voice_id": CRAZY_HORSE_VOICE_ID,
        "visual_cue": "Black Hills / Paha Sapa landscape - gentle zoom on pines and river",
        "filename": "02_crazy_horse.mp3"
    },
    {
        "id": 3,
        "character": "Shaka Zulu",
        "section_name": "Zulu Kingdom Description",
        "text": """Our land was a place of a thousand green hills that rolled across the earth like waves on a great ocean. The grass grew tall and sweet — perfect for our cattle to graze.

In the early mornings, a thick white mist would wrap itself around the mountain peaks like a warm blanket. Then the sun would rise and cut through the mist with golden light.

We built our villages, which we called kraals, in circles on the ridges of those hills. The land gave us everything. It gave us wood to make our shields and spears. It gave us iron from the soil.

When our warriors ran across those hills, it felt like the earth itself was beating like a strong heart beneath their feet.

We did not just live on the land. We were part of it. It shaped who we were as a people.""",
        "voice_id": SHAKA_ZULU_VOICE_ID,
        "visual_cue": "Zulu Kingdom rolling green hills with morning mist and kraal",
        "filename": "03_shaka_zulu.mp3"
    },
    {
        "id": 4,
        "character": "General Custer",
        "section_name": "American West Perspective",
        "text": """To us, those vast plains and rolling hills represented opportunity and the future of our growing nation.

We saw wide, open grasslands that could one day become farms and towns for American families moving westward. We believed it was our duty to help explore and protect this new frontier.

The Black Hills, in particular, were seen as a place of great promise because of the gold discovered there. We viewed the land as something that could help build a stronger, larger country.

Many of us felt we were part of an important mission — opening up new opportunities for settlers and helping the United States grow.""",
        "voice_id": CUSTER_VOICE_ID,
        "visual_cue": "Wide shot of American plains / Black Hills from frontier perspective",
        "filename": "04_custer.mp3"
    },
    {
        "id": 5,
        "character": "Uncle Billy Bobby",
        "section_name": "Primary Sources Teaching Moment",
        "text": """Kids, before we finish, I want to teach you something really important about history.

The stories you just heard didn’t come from me making things up. They come from what people who were actually there said or wrote. These are called primary sources.

A primary source is like a diary, a letter, a treaty, or a story told by someone who lived through the moment. It’s the closest thing we have to hearing their real voice.

When we look at primary sources, we can better understand why someone loved their land so much, or why someone else saw it as a new beginning.

This helps us heal. It helps us see that everyone had reasons that made sense to them. And when we understand each other better, we can respect one another more — even when we disagree.

This year, in 2026, the United States Senate passed a resolution commemorating the 150th anniversary of these events. It shows that people are still thinking about this history and trying to understand it from many different sides — just like we’re doing today.

That’s why primary sources are so powerful. They let the people who lived the story speak for themselves.""",
        "voice_id": UNCLE_BILLY_VOICE_ID,
        "visual_cue": "Return to warm campfire scene with all characters",
        "filename": "05_primary_sources.mp3"
    },
    {
        "id": 6,
        "character": "Uncle Billy Bobby",
        "section_name": "Closing & Reflection",
        "text": """Thank you to Crazy Horse, Shaka Zulu, and General Custer for helping us see these landscapes through their eyes.

Remember, the next time you hear about history or see a place on a map, try to imagine what that land might have meant to the people who lived there.

Home isn’t just a spot on the ground — it’s the stories, the memories, and the love people have for it.

Thanks for listening to The TUZ Podcast. I’m Uncle Billy Bobby.

Keep exploring, keep asking questions, and remember to respect everyone’s story.""",
        "voice_id": UNCLE_BILLY_VOICE_ID,
        "visual_cue": "Final wide shot of campfire - slow fade out",
        "filename": "06_uncle_closing.mp3"
    }
]

# ====================== GENERATE AUDIO ======================

# Note: using `generate_audio` from `eleven_audio.py` which handles
# API key lookup, timeouts, and error reporting.

# ====================== MAIN EXECUTION ======================

def main(dry_run: bool = False, force: bool = False, retries: int = 3, backoff: float = 1.0):
    print("Generating TUZ Episode Audio + Updated JSON Data Feed (with S.Res.795)...\n")

    generated_files = []

    for section in sections:
        out_path = os.path.join(OUTPUT_FOLDER, section["filename"])

        if dry_run:
            # Create a small placeholder file (do not call the API)
            placeholder_path = out_path + ".dryrun.txt"
            preview = section["text"][:400].replace("\n", " ")
            with open(placeholder_path, "w", encoding="utf-8") as ph:
                ph.write(f"DRY RUN: Would generate audio for '{section['section_name']}'\n\n")
                ph.write(preview)
            print(f"ℹ️ Dry-run: would generate {out_path} (placeholder at {placeholder_path})")
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
            # store filename and metadata (keep original section dict)
            episode_data["sections"].append(section)
            generated_files.append(out_path)

    # Save JSON data feed
    json_path = os.path.join(OUTPUT_FOLDER, "tuz_episode_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(episode_data, f, indent=2, ensure_ascii=False)

    # Optionally combine generated clips into one episode MP3 (skip for dry-run placeholders)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_filename = f"TUZHorizonLine_{timestamp}.mp3"
    combined_path = os.path.join(OUTPUT_FOLDER, combined_filename)
    real_audio_files = [p for p in generated_files if p.endswith('.mp3')]
    if real_audio_files:
        try:
            combine_into_one_mp3(real_audio_files, combined_path, silence_ms=400)
            print(f"   Combined episode created at: {combined_path}")
        except Exception as e:
            print(f"⚠️ Failed to combine files: {e}")

    print(f"\n🎉 Done!")
    print(f"   Audio files saved in: {OUTPUT_FOLDER}/")
    print(f"   JSON data feed saved as: {json_path}")
    print(f"   Total sections: {len(episode_data['sections'])}")
    print(f"   S.Res.795 reference included in Primary Sources section.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TUZ episode audio (uses ElevenLabs).")
    parser.add_argument("--dry-run", action="store_true", help="Do not call the API; write placeholders and JSON only.")
    parser.add_argument("--force", action="store_true", help="Allow live API calls (required for real generation).")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries for transient HTTP errors (default: 3)")
    parser.add_argument("--backoff", type=float, default=1.0, help="Exponential backoff base in seconds (default: 1.0)")
    args = parser.parse_args()
    # Pass the flags into main so the safety gate and retry behavior are enforced
    main(dry_run=args.dry_run, force=args.force, retries=args.retries, backoff=args.backoff)