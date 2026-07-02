import os
import pytest

import eleven_audio


class DummyResponse:
    def __init__(self, status_code=500, text="", content=b""):
        self.status_code = status_code
        self.text = text
        self.content = content


def test_generate_audio_retries_and_success(tmp_path, monkeypatch):
    out_file = tmp_path / "out.mp3"

    # First two calls return 500, third call returns 200 with content
    responses = [DummyResponse(500, "server error"), DummyResponse(500, "server error"), DummyResponse(200, "OK", content=b"audio-bytes")]

    def fake_post(*args, **kwargs):
        return responses.pop(0)

    monkeypatch.setattr(eleven_audio.requests, "post", fake_post)

    # Ensure API key is set for test
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    success = eleven_audio.generate_audio("hello world", "voice-id", str(out_file), retries=3, backoff_factor=0.01)
    assert success
    assert out_file.exists()
    assert out_file.read_bytes() == b"audio-bytes"


def test_generate_audio_gives_up_after_retries(tmp_path, monkeypatch):
    out_file = tmp_path / "out2.mp3"

    # All responses are 500
    def fake_post(*args, **kwargs):
        return DummyResponse(500, "server error")

    monkeypatch.setattr(eleven_audio.requests, "post", fake_post)
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    success = eleven_audio.generate_audio("hello", "v", str(out_file), retries=2, backoff_factor=0.01)
    assert success is False
    assert not out_file.exists()
