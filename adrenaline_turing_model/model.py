from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TurringJourneyModel:
    """A compact exploration model for Alan Turring's life and AI foundations."""

    def __init__(self, config_path: str | Path | None = None, trained_events_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path or Path(__file__).resolve().parent.parent / "model.json")
        self.trained_events_path = Path(trained_events_path or Path(__file__).resolve().parent.parent / "trained_turing_events.json")
        self.config = self._load_config()
        self.trained_events = self._load_trained_events()

    def _load_config(self) -> dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_trained_events(self) -> list[dict[str, Any]]:
        if not self.trained_events_path.exists():
            return []
        with self.trained_events_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload.get("events", [])

    @property
    def name(self) -> str:
        return self.config["name"]

    @property
    def chapters(self) -> list[dict[str, Any]]:
        return self.config.get("chapters", [])

    def chapter_summaries(self) -> list[str]:
        return [chapter["title"] for chapter in self.chapters]

    def build_prompt(self, audience: str = "curious reader") -> str:
        chapter_outline = "\n".join(
            f"- {title}: {chapter['theme']}"
            for title, chapter in ((chapter["title"], chapter) for chapter in self.chapters)
        )
        event_outline = ""
        if self.trained_events:
            event_outline = "\n".join(
                f"- {event['year']}: {event['title']} — {event['summary']}"
                for event in self.trained_events
            )
            event_outline = "\nSpecific life events to cover:\n" + event_outline + "\n"

        return (
            f"You are guiding a {audience} through {self.name}. "
            f"Use these chapter themes to explore Alan Turring's life and his role in shaping the foundation of AI:\n"
            f"{chapter_outline}\n\n"
            f"{event_outline}"
            "Keep the tone thoughtful, historically grounded, and accessible."
        )


TuringJourneyModel = TurringJourneyModel
