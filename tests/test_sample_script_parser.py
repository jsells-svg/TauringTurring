import GenerateAudioFromSampleScript as generator


def test_parse_samplescript_preserves_dialogue_order_and_voice_ids(tmp_path):
    script_path = tmp_path / "screenplay.txt"
    script_path.write_text(
        """UNCLE BILLY BOBBY
Welcome to the show.

Billy Bobby gestures to his guests.

HARRIET TUBMAN
(Leaning forward)
Glad to be here.

WINSTON CHURCHILL
Quite. I can lend a strategic ear.

UNCLE BILLY BOBBY
Thanks for joining us.

**FADE OUT.**
""",
        encoding="utf-8",
    )

    sections = generator.parse_samplescript(str(script_path))

    assert [section["character"] for section in sections] == [
        "Uncle Billy Bobby",
        "Harriet Tubman",
        "Winston Churchill",
        "Uncle Billy Bobby",
    ]
    assert [section["voice_id"] for section in sections] == [
        generator.UNCLE_BILLY_VOICE_ID,
        generator.GUEST_1_VOICE_ID,
        generator.GUEST_2_VOICE_ID,
        generator.UNCLE_BILLY_VOICE_ID,
    ]
    assert "gestures to his guests" not in sections[0]["text"]
    assert sections[1]["text"] == "Glad to be here."
