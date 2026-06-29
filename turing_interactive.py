"""
Interactive Turing Model Application
Engages users in a conversation about Alan Turing's life and AI foundations.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from adrenaline_turing_model.model import TurringJourneyModel


class TuringConversation:
    """Interactive conversation engine for exploring Alan Turing's life."""

    def __init__(self, enable_tts: bool = False) -> None:
        self.model = TurringJourneyModel()
        self.enable_tts = enable_tts
        self.current_chapter_idx = 0
        self.visited_chapters = set()
        self.conversation_history: list[dict[str, str]] = []

        if self.enable_tts:
            try:
                import pyttsx3

                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)
            except ImportError:
                print("⚠️  pyttsx3 not available. Text-to-speech disabled.")
                self.enable_tts = False
            except Exception as e:
                print(f"⚠️  TTS initialization failed: {e}. Continuing without audio.")
                self.enable_tts = False

    def speak(self, text: str) -> None:
        """Synthesize speech if TTS is enabled."""
        if self.enable_tts:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"(TTS error: {e})")

    def display_welcome(self) -> None:
        """Display welcome message and setup."""
        print("\n" + "=" * 80)
        print("🤖 ALAN TURING INTERACTIVE EXPERIENCE 🤖".center(80))
        print("=" * 80)
        print("\nWelcome! You're about to explore the life and legacy of Alan Turing,")
        print("one of the most influential mathematicians and computer scientists.")
        print("\nCommands:")
        print("  'next'  - Move to next chapter")
        print("  'prev'  - Move to previous chapter")
        print("  'list'  - Show all chapters")
        print("  'events'- See historical events from the model")
        print("  'help'  - Show this help menu")
        print("  'quit'  - Exit the application")
        print("\nOtherwise, type a question or comment about Turing's life.\n")
        print("=" * 80 + "\n")
        self.speak(
            "Welcome to the Alan Turing Interactive Experience. "
            "You can ask questions or explore his life and legacy."
        )

    def display_chapter(self, idx: int) -> None:
        """Display current chapter information."""
        chapters = self.model.chapters
        if idx < 0 or idx >= len(chapters):
            print("Invalid chapter index.")
            return

        chapter = chapters[idx]
        self.current_chapter_idx = idx
        self.visited_chapters.add(idx)

        print(f"\n📖 Chapter {idx + 1}: {chapter['title'].upper()}")
        print(f"Theme: {chapter['theme']}")
        print("-" * 80)
        print("Key questions to explore:")
        for q in chapter.get("questions", []):
            print(f"  • {q}")
        print()

        # Display related trained events
        events = self.model.trained_events
        if events:
            relevant_events = [
                e
                for e in events
                if any(kw in chapter["title"].lower() for kw in e.get("title", "").lower().split())
            ]
            if relevant_events:
                print("Historical events in this chapter:")
                for event in relevant_events[:3]:
                    print(f"  [{event['year']}] {event['title']} — {event['summary'][:60]}...")
                print()

    def show_chapters_list(self) -> None:
        """Show all available chapters."""
        print("\n📚 AVAILABLE CHAPTERS:")
        print("-" * 80)
        for idx, chapter in enumerate(self.model.chapters):
            status = "✓" if idx in self.visited_chapters else " "
            print(f"  [{status}] Chapter {idx + 1}: {chapter['title']}")
        print()

    def show_events(self) -> None:
        """Display trained historical events."""
        if not self.model.trained_events:
            print("\nNo trained events available.\n")
            return

        print("\n📅 HISTORICAL EVENTS:")
        print("-" * 80)
        for event in self.model.trained_events:
            print(f"  [{event['year']}] {event['title']}")
            print(f"       {event['summary']}\n")

    def generate_response(self, user_input: str) -> str:
        """Generate a contextual response to user input."""
        chapter = self.model.chapters[self.current_chapter_idx]
        chapter_context = f"We're currently exploring: {chapter['title']} ({chapter['theme']})"

        prompt = (
            f"You are an expert guide on Alan Turing's life and work. {chapter_context}. "
            f"The user asks: '{user_input}'\n\n"
            f"Provide a thoughtful, historically accurate response (2-3 sentences) that:\n"
            f"- Relates to this chapter's theme\n"
            f"- Educates about Turing's life or work\n"
            f"- Connects to the foundation of artificial intelligence\n\n"
            f"Response:"
        )

        # Simulate response (in a real system, this would call an LLM)
        response = (
            f"That's an excellent question about the '{chapter['title']}' period. "
            f"Based on Turing's work and life during this time, we see how {chapter['theme'].lower()} "
            f"was crucial to his development and legacy. This relates directly to the foundations of AI "
            f"that he helped establish."
        )

        return response

    def run_interactive(self) -> None:
        """Main interactive loop."""
        self.display_welcome()
        self.display_chapter(0)

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                cmd = user_input.lower()

                if cmd in {"quit", "exit"}:
                    print("\n👋 Thank you for exploring Alan Turing's legacy!")
                    self.speak("Thank you for exploring Alan Turring's legacy. Goodbye.")
                    break

                elif cmd == "help":
                    self.display_welcome()

                elif cmd == "next":
                    if self.current_chapter_idx < len(self.model.chapters) - 1:
                        self.display_chapter(self.current_chapter_idx + 1)
                    else:
                        print("You're at the last chapter.")

                elif cmd == "prev":
                    if self.current_chapter_idx > 0:
                        self.display_chapter(self.current_chapter_idx - 1)
                    else:
                        print("You're at the first chapter.")

                elif cmd == "list":
                    self.show_chapters_list()

                elif cmd == "events":
                    self.show_events()

                else:
                    # Generate response to user query
                    response = self.generate_response(user_input)
                    print(f"\n🔵 Turing Guide: {response}\n")
                    self.speak(response)
                    self.conversation_history.append(
                        {"user": user_input, "assistant": response}
                    )

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                self.speak("Goodbye.")
                break
            except Exception as e:
                print(f"Error: {e}\n")


def main() -> None:
    """Entry point for the Turing interactive experience."""
    # Check for command-line arguments
    enable_tts = "--tts" in sys.argv or "-t" in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            "Usage: python turing_interactive.py [OPTIONS]\n\n"
            "Options:\n"
            "  --tts, -t     Enable text-to-speech\n"
            "  --help, -h    Show this help message\n"
        )
        return

    try:
        conversation = TuringConversation(enable_tts=enable_tts)
        conversation.run_interactive()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
