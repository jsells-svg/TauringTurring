import sys
import types
from pathlib import Path

import GenerateScreenplayToVideo as screenplay_video
from GenerateScreenplayToVideo import render_slide_image


def test_render_slide_image_writes_png(tmp_path: Path) -> None:
    out_path = tmp_path / "slide.png"
    block = {"type": "dialogue", "speaker": "NARRATOR", "text": "Hello world"}

    result = render_slide_image(block, out_path)

    assert result == out_path
    assert out_path.exists()
    assert out_path.suffix == ".png"


def test_make_video_uses_tts_returned_audio_path(tmp_path: Path, monkeypatch) -> None:
    screenplay_path = tmp_path / "script.txt"
    screenplay_path.write_text("INT. ROOM - DAY\nNARRATOR: Hello world\n", encoding="utf-8")
    out_video = tmp_path / "out.mp4"

    class DummyClip:
        def __init__(self, path: str):
            self.path = path
            self.duration = 1.0

        def set_duration(self, duration):
            self.duration = duration
            return self

        def set_audio(self, audio):
            self.audio = audio
            return self

    calls = []
    audio_paths = []

    def fake_tts(text: str, voice: str, out_path, api_key=None):
        audio_path = Path(str(out_path)).with_suffix(".wav")
        audio_path.write_bytes(b"wav-data")
        calls.append(str(out_path))
        return audio_path

    def fake_audio_clip(path: str):
        audio_paths.append(path)
        return DummyClip(path)

    def fake_image_clip(path: str):
        return DummyClip(path)

    def fake_concatenate(clips, method: str):
        return types.SimpleNamespace(write_videofile=lambda *args, **kwargs: None)

    fake_moviepy = types.ModuleType("moviepy")
    fake_moviepy.AudioFileClip = fake_audio_clip
    fake_moviepy.ImageClip = fake_image_clip
    fake_moviepy.concatenate_videoclips = fake_concatenate
    monkeypatch.setitem(sys.modules, "moviepy", fake_moviepy)
    monkeypatch.setattr(screenplay_video, "render_slide_image", lambda block, out_path, size=(1280, 720): out_path)
    monkeypatch.setattr(screenplay_video, "text_to_speech", fake_tts)

    screenplay_video.make_video(screenplay_path, out_video, voice="alloy")

    assert calls
    assert all(Path(call).suffix == ".mp3" for call in calls)
    assert audio_paths
    assert all(Path(path).suffix == ".wav" for path in audio_paths)
