from parsle import Wordle

TEXT_PASS_2 = """Wordle 1.022 2/6

🟨⬛🟨⬛⬛
🟩🟩🟩🟩🟩"""

# With the 1.000 emoji
TEXT_PASS_4 = """Wordle 1.000 🎉 4/6

⬜️⬜️🟩🟨🟩
⬜️🟩🟩⬜️🟩
⬜️🟩🟩⬜️🟩
🟩🟩🟩🟩🟩"""

# In hard mode
TEXT_PASS_5_HARD = """Wordle 1.000 4/6*

⬜️⬜️🟩🟨🟩
🟩🟩🟩🟩🟩"""

# With a comma as thousands separator
TEXT_FAIL = """Wordle 1,022 X/6

⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜"""


def test_parse_success():
    result = Wordle(TEXT_PASS_2)
    assert result.is_winning()
    assert result.name == "Wordle"
    assert result.age == 1022
    assert result.tries == 2
    assert Wordle(TEXT_PASS_4).tries == 4


def test_parse_fail():
    result = Wordle(TEXT_FAIL)
    assert not result.is_winning()
    assert result.tries == None
    assert result.age == 1022


def test_comparison():
    assert Wordle(TEXT_FAIL) < Wordle(TEXT_PASS_4) < Wordle(TEXT_PASS_2) < Wordle(TEXT_PASS_5_HARD)
