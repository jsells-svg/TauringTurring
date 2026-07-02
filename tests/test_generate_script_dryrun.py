import os
import pytest

import GenerateAudioFromScripttoElevenLabs as gen_script


def test_dry_run_creates_placeholders(tmp_path, monkeypatch):
    # Redirect OUTPUT_FOLDER to temp dir
    monkeypatch.setattr(gen_script, "OUTPUT_FOLDER", str(tmp_path))

    # Ensure no API key is required for dry run
    gen_script.episode_data["sections"] = []

    gen_script.main(dry_run=True)

    # Check placeholder files created for each section
    placeholders = list(tmp_path.glob("*.dryrun.txt"))
    assert len(placeholders) == len(gen_script.sections)

    # Check JSON feed exists
    json_file = tmp_path / "tuz_episode_data.json"
    assert json_file.exists()
    data = json_file.read_text(encoding="utf-8")
    assert "The Landscapes We Loved" in data
