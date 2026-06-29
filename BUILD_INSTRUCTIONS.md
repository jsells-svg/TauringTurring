# Building the Turing Interactive Executable

This guide explains how to build a standalone executable file that loads the Turing Model and engages users about Alan Turing's life.

## Overview

The `turing_interactive.py` application provides an interactive experience where users can:
- Explore Alan Turing's life through structured chapters
- Ask questions about his work and legacy
- Navigate through historical events
- Optionally use text-to-speech (TTS) to hear responses read aloud

## Prerequisites

1. **Virtual Environment**: Ensure you're using the project's Python virtual environment
2. **Dependencies**: All required packages should be installed from `requirements.txt`
3. **PyInstaller**: Will be installed automatically during the build process

## Quick Start

### Option 1: Using PowerShell (Recommended for Windows)

```powershell
# Activate the virtual environment (if not already active)
.\Scripts\Activate.ps1

# Run the build script
.\build_executable.ps1
```

### Option 2: Using Command Prompt

```cmd
# Activate the virtual environment (if not already active)
.\Scripts\activate.bat

# Run the build script
.\build_executable.bat
```

### Option 3: Manual Build

```powershell
# Activate virtual environment
.\Scripts\Activate.ps1

# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --clean --onefile turing_interactive.spec
```

## Build Output

After a successful build, the executable will be located at:

```
.\dist\TuringInteractive.exe
```

## Running the Executable

### Basic Usage

```powershell
.\dist\TuringInteractive.exe
```

This launches the interactive Turing application in console mode.

### With Text-to-Speech

```powershell
.\dist\TuringInteractive.exe --tts
```

or

```powershell
.\dist\TuringInteractive.exe -t
```

This enables audio synthesis of responses (requires `pyttsx3`).

### Show Help

```powershell
.\dist\TuringInteractive.exe --help
```

## Interactive Commands

Once the application is running, use these commands:

| Command | Description |
|---------|-------------|
| `next` | Move to the next chapter |
| `prev` | Move to the previous chapter |
| `list` | Show all available chapters |
| `events` | Display historical events from the model |
| `help` | Show the help menu |
| `quit` or `exit` | Exit the application |
| *(any text)* | Ask a question about Turing's life |

## Chapters Available

The application guides users through these chapters:

1. **Early Curiosity** - Education and mathematical insight
2. **War and Secrecy** - Codebreaking and Bletchley Park
3. **The Machine Concept** - The Turing machine and computability
4. **The Imitation Game** - Machine intelligence and AI
5. **Legacy and Reflection** - History, recognition, and ethical impact

## Troubleshooting

### Build Fails with "pyinstaller not found"

Make sure PyInstaller is installed:

```powershell
pip install pyinstaller
```

### "Virtual environment not activated"

Activate the environment first:

```powershell
.\Scripts\Activate.ps1  # PowerShell
# or
.\Scripts\activate.bat  # Command Prompt
```

### Executable doesn't run / "module not found"

Ensure the virtual environment is active before running the executable:

```powershell
.\Scripts\Activate.ps1
.\dist\TuringInteractive.exe
```

### Text-to-speech not working

TTS requires `pyttsx3`. If it's not working:

```powershell
pip install pyttsx3
```

Then rebuild the executable.

## Customization

To modify the build configuration, edit `turing_interactive.spec`:

- Change `name='TuringInteractive'` to use a different executable name
- Modify `console=True` to `console=False` to hide the console window
- Add or remove data files in the `datas` list

After modifying the spec file, rebuild using:

```powershell
pyinstaller --clean --onefile turing_interactive.spec
```

## Distribution

The standalone executable in `.\dist\TuringInteractive.exe` can be:
- Shared with others
- Copied to any Windows system with Python 3.8+
- Compressed and distributed as an archive

The executable contains all necessary dependencies and doesn't require a Python installation on the target system.

## Technical Details

### Build Process

1. PyInstaller analyzes `turing_interactive.py` and its dependencies
2. It collects required data files (`model.json`, `trained_turing_events.json`, etc.)
3. Bundles everything into a single executable
4. The `--onefile` option creates a single `.exe` instead of a directory

### Data Files Included

The executable bundles:
- `model.json` - Model configuration and chapter definitions
- `trained_turing_events.json` - Historical events and timeline
- `adrenaline_turing_model/` - The model module
- All dependencies from `requirements.txt`

## Next Steps

1. Build the executable using one of the methods above
2. Test it locally with: `.\dist\TuringInteractive.exe`
3. Share the executable or distribute via installer tools like NSIS or WiX
