from pathlib import Path

from adrenaline_turing_model.training import TurringEventTrainer


if __name__ == "__main__":
    trainer = TurringEventTrainer(
        data_path=Path("data/turing_life_events.json"),
        output_path=Path("trained_turing_events.json"),
    )
    compiled = trainer.train()
    print(f"Trained on {compiled['event_count']} events")
    print(trainer.build_training_prompt(audience="reader"))
