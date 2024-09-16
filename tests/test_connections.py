from parsle import Connections

TEXT_PASS_0 = """Connections
Puzzle #462
🟩🟩🟩🟩
🟨🟨🟨🟨
🟦🟦🟦🟦
🟪🟪🟪🟪"""

TEXT_PASS_2 = """Connections
Puzzle #462
🟩🟩🟩🟩
🟪🟦🟨🟪
🟨🟨🟨🟨
🟦🟦🟦🟪
🟦🟦🟦🟦
🟪🟪🟪🟪"""

# With a comma as thousands separator
TEXT_FAIL = """Connections
Puzzle #463
🟨🟨🟨🟨
🟩🟩🟩🟦
🟩🟩🟩🟩
🟪🟦🟦🟦
🟪🟦🟦🟦
🟪🟦🟦🟦"""


def test_parse_success():
    result = Connections(TEXT_PASS_2)
    assert result.name == "Connections"
    assert result.age == 462
    assert result.mistakes == 2
    assert result.is_winning()
    assert Connections(TEXT_PASS_0).mistakes == 0


def test_parse_fail():
    result = Connections(TEXT_FAIL)
    assert result.mistakes == 4
    assert not result.is_winning()


def test_comparison():
    assert Connections(TEXT_FAIL) < Connections(TEXT_PASS_2) < Connections(TEXT_PASS_0)
