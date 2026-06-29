#!/usr/bin/env pwsh
# Build script for Turing Interactive Executable (PowerShell version)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Turing Interactive - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "ERROR: Virtual environment not activated!" -ForegroundColor Red
    Write-Host "Please activate the virtual environment first:" -ForegroundColor Yellow
    Write-Host "  .\Scripts\Activate.ps1"
    exit 1
}

Write-Host "[1/3] Installing PyInstaller..." -ForegroundColor Green
python -m pip install pyinstaller -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}

Write-Host "[2/3] Building executable..." -ForegroundColor Green
Write-Host ""
pyinstaller --clean --onefile turing_interactive.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable Location: .\dist\TuringInteractive.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "Usage:"
Write-Host "  .\dist\TuringInteractive.exe          - Run the interactive application"
Write-Host "  .\dist\TuringInteractive.exe --tts    - Run with text-to-speech enabled"
Write-Host "  .\dist\TuringInteractive.exe --help   - Show help menu"
Write-Host ""
