# Alan Turing Exploration Model

An interactive project for exploring the life, work, and historical importance of Alan Turing, with optional text-to-speech, slide generation, and video export.

## Overview

This repository contains a prototype experience that presents Alan Turing's story through:
- an interactive Python application,
- structured timeline/model data,
- generated slides,
- optional ElevenLabs voice synthesis,
- and MP4 video rendering.

The goal is to make Turing's legacy more accessible while providing a reusable pipeline for educational storytelling.

## Repository contents

- `interactive_demo.py` — interactive demo entry point
- `turing_interactive.py` — interactive Turing experience
- `model.json` — structured model definition
- `timeline.md` — timeline content source
- `trained_turing_events.json` — processed event data
- `generate_slides.py` — creates slide assets from timeline content
- `generate_video.py` — renders timeline slides and audio into video
- `eleven_api.py` — helper for ElevenLabs text-to-speech
- `train_model.py` — model/training utility
- `requirements.txt` — Python dependencies
- `BUILD_INSTRUCTIONS.md` — executable build instructions
- `QUICKSTART.md` — quick usage guide

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt