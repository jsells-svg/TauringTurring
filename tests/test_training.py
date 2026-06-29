import json
import tempfile
import unittest
from pathlib import Path

from adrenaline_turing_model.training import TurringEventTrainer


class TurringEventTrainerTests(unittest.TestCase):
    def test_training_creates_compiled_event_knowledge(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "trained_events.json"
            trainer = TurringEventTrainer(
                data_path=Path("data/turing_life_events.json"),
                output_path=output_path,
            )

            compiled = trainer.train()
            self.assertEqual(compiled["event_count"], 6)
            self.assertTrue(output_path.exists())

            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["event_count"], 6)
            self.assertIn("Bletchley Park", saved["events"][1]["title"])

    def test_training_prompt_mentions_specific_events(self) -> None:
        trainer = TurringEventTrainer(data_path=Path("data/turing_life_events.json"))
        prompt = trainer.build_training_prompt(audience="student")

        self.assertIn("student", prompt)
        self.assertIn("1936", prompt)
        self.assertIn("Bletchley Park", prompt)


if __name__ == "__main__":
    unittest.main()
