from __future__ import annotations

from adrenaline_turing_model.model import TurringJourneyModel


def main() -> None:
    model = TurringJourneyModel()
    print("Turring Interactive Demo")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break

        prompt = model.build_prompt(audience="student")
        response = (
            f"{prompt}\n\n"
            f"User question: {user_input}\n\n"
            "Suggested response: Discuss the historical context, explain the significance of the event, and connect it to the foundations of AI."
        )
        print("Turring:", response)
        print("-" * 80)


if __name__ == "__main__":
    main()
