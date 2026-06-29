from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TurringEventTrainer:
    """Compile a curated set of life events into a reusable training artifact."""

    def __init__(self, data_path: str | Path | None = None, output_path: str | Path | None = None) -> None:
        self.data_path = Path(data_path or Path(__file__).resolve().parent.parent / "data" / "turing_life_events.json")
        self.output_path = Path(output_path or Path(__file__).resolve().parent.parent / "trained_turing_events.json")
        self.events = self._load_events()

    def _load_events(self) -> list[dict[str, Any]]:
        with self.data_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def train(self) -> dict[str, Any]:
        compiled = {
            "model": "alan-turring-life-and-ai-foundations",
            "event_count": len(self.events),
            "events": self.events,
            "summary": "A curated knowledge base of specific events from Alan Turring's life.",
        }
        self.output_path.write_text(json.dumps(compiled, indent=2), encoding="utf-8")
        return compiled

    def build_training_prompt(self, audience: str = "reader") -> str:
        event_lines = "\n".join(
            f"- {event['year']}: {event['title']} — {event['summary']}"
            for event in self.events
        )
        return (
            f"You are guiding a {audience} through Alan Turring's life. "
            "Use the following specific historical events as anchors for the narrative:\n"
            f"{event_lines}\n\n"
            "Keep the storytelling grounded in facts, clear, and reflective."
        )


TuringEventTrainer = TurringEventTrainer
