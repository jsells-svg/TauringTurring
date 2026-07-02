# Alan Turring Exploration Model

This workspace contains a complete interactive experience for exploring Alan Turring's life and his role in laying the conceptual groundwork for artificial intelligence.

## Quick Start: Run the Executable

The easiest way to engage with the Turing Model is to run the interactive executable:

```powershell
.\dist\TuringInteractive.exe
```

Or with text-to-speech enabled:

```powershell
.\dist\TuringInteractive.exe --tts
```

👉 **See [QUICKSTART.md](QUICKSTART.md) for details on using the interactive experience.**

## What is included

- **Interactive Executable** (`dist/TuringInteractive.exe`) - Standalone app to engage users about Turing's life
- **Interactive Python Module** (`turing_interactive.py`) - The underlying interactive experience
- A structured model definition in [model.json](model.json)
- A Python module in [adrenaline_turing_model/model.py](adrenaline_turing_model/model.py)
- A small verification test in [tests/test_model.py](tests/test_model.py)

## Run the model

### Using Python directly

From the workspace root:

```powershell
.\Scripts\python.exe -m unittest discover -s tests -v
```

You can also inspect the generated prompt with:

```powershell
.\Scripts\python.exe -c "from adrenaline_turing_model.model import TurringJourneyModel; print(TurringJourneyModel().build_prompt())"
```

Or run the interactive Python module:

```powershell
.\Scripts\python.exe turing_interactive.py --tts
```

### Building a New Executable

To rebuild the standalone executable after making changes:

```powershell
.\Scripts\Activate.ps1
.\build_executable.ps1
```

👉 **See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed build instructions.**

## Eleven Labs audio and secure key handling

This project can make audio using Eleven Labs. There are two scripts for this:

- `eleven_api.py` — a helper function for single text-to-speech calls.
- `generate_video.py` — makes audio for the timeline and creates `Turring_Timeline.mp4`.
- `GenerateAudioFromScripttoElevenLabs.py` — makes several clips and combines them into one MP3 from a simple config file.

### Why this is safe

In the corporate world, storing secret keys in plain text files is not safe. The best way is:

1. Put the key into an environment variable.
2. Or store it in the system keyring.
3. Do not save the key in a text file that others can open.

This project supports all three methods.

---

## KeyCommands

Use this quick list when setting up your Eleven Labs API key and audio generation.

```powershell
# 1) Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2) Store the key in the system keyring (recommended)
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --api-key "<your_api_key>" --store-key

# 3) Validate the key
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --validate-key

# 4) Check ffmpeg installation
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --check-ffmpeg

# 5) Run full setup checks for both key and ffmpeg
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --setup

# 6) Generate audio from config
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --config audio_config_example.json
```

---

## Step 1: Install the tools you need

Open PowerShell and run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This makes sure your Python environment has the packages needed for:

- `requests` — talk to Eleven Labs
- `PyYAML` — read YAML config files
- `keyring` — store your secret key safely

You also need `ffmpeg` installed on your computer and on the PATH.

---

## Step 2: Save your Eleven Labs key safely

### Option A: Use an environment variable

This is the easiest and safest way.

In PowerShell:

```powershell
$env:ELEVENLABS_API_KEY="<your_api_key>"
```

Now the script can read the key without putting it in a file.

### Option B: Store the key in the system keyring

If you want an extra safety layer, save the key to the OS keyring once.

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --api-key "<your_api_key>" --store-key
```

After this, the script can use the key from the keyring automatically.

### Option C: Do not use text files for keys

This README does not recommend saving the API key in a normal text file such as `key.txt`.
If someone else gets access to your computer, they could read it.

---

## Step 3: Check the key is valid

Before you generate audio, make sure Eleven Labs accepts your key.

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --api-key "<your_api_key>" --validate-key
```

If the key is good, the script will say "API key validated successfully." If not, it will tell you the problem.

---

## Step 4: Set up the voice and text config

There is an example file called `audio_config_example.json`.

Open it and replace the placeholders with your real voice IDs and text.

A voice ID is the voice you want Eleven Labs to use, such as a voice name or UUID.

Example config:

```json
{
  "voice_ids": {
    "uncle_billy": "your_uncle_billy_voice_id",
    "crazy_horse": "your_crazy_horse_voice_id",
    "shaka_zulu": "your_shaka_zulu_voice_id"
  },
  "texts": {
    "uncle_opening": "Uncle Billy opens the episode with a short intro.",
    "crazy_horse": "Crazy Horse speaks about the plains.",
    "shaka_zulu": "Shaka Zulu recounts a battle.",
    "uncle_closing": "Uncle Billy closes the episode."
  },
  "output": {
    "combined_filename": "TUZ_Podcast_Landscapes_We_Loved.mp3",
    "silence_ms": 400
  }
}
```

If you want, you can also use a YAML file instead of JSON.

---

## Step 5: Run the audio generation script

When your key is stored and your config file is ready, run:

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --config audio_config_example.json
```

If you use the keyring, you do not need to pass `--api-key` again.

If you want to use the key directly for just one run, you can do:

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --api-key "<your_api_key>" --config audio_config_example.json
```

---

## How the script finds your key

The script looks for the key in this order:

1. `--api-key` command-line option
2. `ELEVENLABS_API_KEY` environment variable
3. `XI_API_KEY` environment variable
4. system keyring

This means the key is never stored in the script itself.

---

## Recommended key management options

| Option | How to use it | Security level | Use when |
|---|---|---|---|
| System keyring | `--store-key` once, then run normally | Best | You want the key stored securely on your machine |
| Environment variable | `$env:ELEVENLABS_API_KEY="<key>"` | Good | You need a simple secure method for this session |
| Command-line `--api-key` | `--api-key "<key>"` | Acceptable | You need a one-off test or validation |
| Plain text file | Not recommended | Weak | Avoid in corporate / shared environments |

> Best practice: use the keyring when possible, and avoid plain-text API key files.

---

## If you want to use voice IDs from environment variables

You can do this too:

```powershell
$env:UNCLE_BILLY_VOICE_ID="<voice_id>"
$env:CRAZY_HORSE_VOICE_ID="<voice_id>"
$env:SHAKA_ZULU_VOICE_ID="<voice_id>"
```

Then the script will use those values instead of the config file voice IDs.

---

## Check ffmpeg installation

Before running the script, make sure `ffmpeg` is installed and on your PATH.

In PowerShell, run:

```powershell
ffmpeg -version
```

If that shows version information, your system has ffmpeg.

You can also ask the script to check for ffmpeg directly:

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --check-ffmpeg
```

If the script returns "✅ ffmpeg is installed and available on PATH.", then you're good.

You can also run the full setup check for both ffmpeg and the Eleven Labs API key:

```powershell
.\.venv\Scripts\python.exe GenerateAudioFromScripttoElevenLabs.py --setup
```

This command will:

- verify `ffmpeg` is installed
- verify your Eleven Labs API key is available
- verify the key is valid with Eleven Labs

---

## Important security advice

- Do not save the Eleven Labs key in a normal text file like `key.txt`.
- Do not paste the key into a public place.
- Use environment variables or the OS keyring.
- If you are using this in a company, ask your security team for the correct way to store secrets.

---

## Troubleshooting

- If the script says the API key is missing, make sure you set `ELEVENLABS_API_KEY` or used `--api-key`.
- If the script says the key is invalid, check the key value and try `--validate-key`.
- If the script says `PyYAML` is missing, run:

```powershell
.\.venv\Scripts\python.exe -m pip install PyYAML
```

- If the script says `keyring` is missing, run:

```powershell
.\.venv\Scripts\python.exe -m pip install keyring
```

- If audio combination fails, make sure `ffmpeg` is installed and on PATH.

---

## Glossary: simple explanations

- **API key**: a secret password for the Eleven Labs service. It tells Eleven Labs who is asking for audio.
- **Environment variable**: a safe place on your computer to keep the API key without writing it in a file.
- **Keyring**: a safe lockbox on your computer where the API key is stored securely.
- **Config file**: a simple file that says which text to speak and which voices to use.
- **Plain text file**: a file like `key.txt`. This is not safe for secrets because anyone can read it.

If you are not sure which option to use, the best choice is the keyring first, then environment variable.
