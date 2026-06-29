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

## Video generation (Eleven Labs)

- `eleven_api.py` — helper to call Eleven Labs text-to-speech (requires `ELEVENLABS_API_KEY`).
- `generate_video.py` — synthesizes audio for each timeline event and stitches slides into `Turring_Timeline.mp4`.

To produce the MP4 (Windows PowerShell example):

```powershell
setx ELEVENLABS_API_KEY "<your_api_key>"
setx ELEVENLABS_VOICE "alloy"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe generate_video.py --timeline timeline.md --out Turring_Timeline.mp4
```

Notes: You must provide a valid Eleven Labs API key and have `ffmpeg` available on PATH for `moviepy`.
