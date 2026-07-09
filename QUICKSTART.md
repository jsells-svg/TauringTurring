# Quick Start - Turing Interactive Executable

## What You Have

A standalone **executable file** that loads the Turing Model and engages users in an interactive conversation about Alan Turing's life and legacy.

**File Location:** `dist/TuringInteractive.exe`

## Running the Executable

### Double-click to run (simplest)

Simply double-click `TuringInteractive.exe` to start the interactive experience.

### From Command Prompt

```cmd
cd c:\ModelAMDRocM\tauringturring
dist\TuringInteractive.exe
```

### With Text-to-Speech (audio responses)

```cmd
dist\TuringInteractive.exe --tts
```

## Generating Episode Audio (TUZ Podcast)

The repository includes `GenerateAudioFromScripttoElevenLabs.py` to generate segmented audio files and a combined episode MP3 using ElevenLabs TTS.

Environment variables required for real generation:
- `ELEVENLABS_API_KEY` or `XI_API_KEY` — your ElevenLabs API key
- `UNCLE_BILLY_VOICE_ID` — ElevenLabs voice ID for Uncle Billy Bobby
- `CRAZY_HORSE_VOICE_ID` — ElevenLabs voice ID for Crazy Horse
- `SHAKA_ZULU_VOICE_ID` — ElevenLabs voice ID for Shaka Zulu
- `CUSTER_VOICE_ID` — ElevenLabs voice ID for General Custer

Set these in PowerShell before running the script:
```powershell
$env:ELEVENLABS_API_KEY = 'sk-1234567890abcdef'
$env:UNCLE_BILLY_VOICE_ID = 'voice-id-uncle-billy'
$env:CRAZY_HORSE_VOICE_ID = 'voice-id-crazy-horse'
$env:SHAKA_ZULU_VOICE_ID = 'voice-id-shaka-zulu'
$env:CUSTER_VOICE_ID = 'voice-id-custer'
```

Dry-run (no API keys required):
```powershell
python GenerateAudioFromScripttoElevenLabs.py --dry-run
```

Real generation (requires API keys and voice IDs). For safety the script refuses to run live calls unless `--force` is supplied. You can tune retry/backoff behavior:
```powershell
python GenerateAudioFromScripttoElevenLabs.py --force --retries 3 --backoff 1.0
```

Output:
- Generated MP3 clips and `tuz_episode_data.json` are written to the `TUZ_Episode_Audio/` folder.
- A combined episode file `TUZ_Podcast_Landscapes_We_Loved.mp3` will be created when real MP3 clips exist.

## Generating Video from a Screenplay
The repository also includes `GenerateScreenplayToVideo.py` for turning a screenplay-style text file into a narrated MP4 using Eleven Labs.

Example usage:
```powershell
$env:ELEVENLABS_API_KEY = 'sk-1234567890abcdef'
python GenerateScreenplayToVideo.py --screenplay screenplay_example.txt --out screenplay_video.mp4 --voice alloy
```

Paste your screenplay into `screenplay_example.txt` using the sample format below. Replace the sample character lines with your own dialogue and scene headings.

To use character-specific voices, create a JSON voice map file and pass it with `--voice-map screenplay_voice_map_example.json`.

If you want specific voices for characters, provide a voice map JSON file like `screenplay_voice_map_example.json`.

## What to Expect

When you run the application, you'll see:

1. **Welcome screen** - Introduction to the experience
2. **Current Chapter** - Information about Alan Turing's life period
3. **Prompt for input** - Ask questions or use commands

### Example Interaction

```
🤖 ALAN TURING INTERACTIVE EXPERIENCE 🤖

📖 Chapter 1: EARLY CURIOSITY
Theme: education and mathematical insight
────────────────────────────────────────────────────────────────────────────────
Key questions to explore:
  • How did Turing's childhood interests shape his later thinking?
  • What made his mathematical approach distinct?

You: What did Turing study as a child?
🔵 Turing Guide: That's an excellent question about the 'Early Curiosity' 
period. Based on Turing's work and life during this time...

You: next
📖 Chapter 2: WAR AND SECRECY
...
```

## Commands

While in the application:

| Command | What it does |
|---------|-------------|
| `next` | Go to next chapter |
| `prev` | Go to previous chapter |
| `list` | Show all chapters |
| `events` | Show historical timeline |
| `help` | Show help menu |
| `quit` or `exit` | Exit the application |
| *(type anything else)* | Ask a question about Turing |

## Chapters Included

1. **Early Curiosity** - Turing's education and mathematical thinking
2. **War and Secrecy** - Bletchley Park and codebreaking
3. **The Machine Concept** - The Turing machine and computation
4. **The Imitation Game** - AI and machine intelligence
5. **Legacy and Reflection** - History and ethical impact

## Features

✅ Interactive navigation through Turing's life  
✅ Historical event timeline  
✅ Question-and-answer interface  
✅ Optional text-to-speech for immersive experience  
✅ Standalone executable (no Python installation needed)  

## Troubleshooting

**The .exe won't start:**
- Make sure you're in the correct directory: `c:\ModelAMDRocM\tauringturring\`
- Try running from Command Prompt to see any error messages
- Ensure you have at least Windows 7 or later

**Text-to-speech doesn't work:**
- This is optional. The app works fine without it.
- It requires the `pyttsx3` library (included in the build)

**It closes immediately:**
- Likely an error. Run from Command Prompt to see the error message
- Make sure `model.json` and `trained_turing_events.json` are in the same folder

## Distribution

You can share this executable with others. It's a standalone file that doesn't require:
- Python installation
- Virtual environment setup  
- Any other dependencies

Just copy `dist/TuringInteractive.exe` to share it!

---

**For detailed build instructions**, see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
