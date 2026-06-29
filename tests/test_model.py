import unittest
from pathlib import Path

from adrenaline_turing_model.model import TurringJourneyModel


class TurringJourneyModelTests(unittest.TestCase):
    def test_model_metadata_and_chapters(self) -> None:
        model = TurringJourneyModel(config_path=Path("model.json"))

        self.assertEqual(model.name, "alan-turring-life-and-ai-foundations")
        self.assertEqual(len(model.chapter_summaries()), 5)
        self.assertIn("The imitation game", model.chapter_summaries())

    def test_prompt_includes_key_topics(self) -> None:
        model = TurringJourneyModel(config_path=Path("model.json"))
        prompt = model.build_prompt(audience="student")

        self.assertIn("student", prompt)
        self.assertIn("Alan Turring", prompt)
        self.assertIn("foundation of ai", prompt.lower())


if __name__ == "__main__":
    unittest.main()
