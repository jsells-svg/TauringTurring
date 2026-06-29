@echo off
REM Build script for Turing Interactive Executable
REM This script builds a standalone executable from the turing_interactive.py file

echo.
echo ========================================
echo Turing Interactive - Build Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment not activated!
    echo Please activate the virtual environment first:
    echo   .\Scripts\activate
    exit /b 1
)

echo [1/3] Installing PyInstaller...
python -m pip install pyinstaller -q
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    exit /b 1
)

echo [2/3] Building executable...
echo.
pyinstaller --clean --onefile turing_interactive.spec

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    exit /b 1
)

echo.
echo [3/3] Build complete!
echo.
echo ========================================
echo Executable Location: .\dist\TuringInteractive.exe
echo ========================================
echo.
echo Usage:
echo   .\dist\TuringInteractive.exe          - Run the interactive application
echo   .\dist\TuringInteractive.exe --tts    - Run with text-to-speech enabled
echo   .\dist\TuringInteractive.exe --help   - Show help menu
echo.
