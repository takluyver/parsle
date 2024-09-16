from dataclasses import dataclass, field
import itertools
import re
from typing import List, Tuple
from .game_result import GameResult


@dataclass
class Strands(GameResult):
    # Blue dot for word found, yellow dot for theme word found,
    # lamp for hint
    sequence: Tuple[str, ...]
    hints: int = field(metadata={"higher_is_better": False})
    tries_before_theme_word: int = field(metadata={"higher_is_better": False})
    hints_before_theme_word: int = field(metadata={"higher_is_better": False})

    def __init__(self, text: str):
        super().__init__("Strands", "https://www.nytimes.com/games/strands")
        match = re.match(r"Strands #(\d+)", text, re.MULTILINE)
        assert match, "Not a Strands game"
        self.age = int(match.group(1))
        assert "🟡" in text, "Not a Strands game"
        self.sequence = tuple(filter(lambda ch: ch in {"🔵", "🟡", "💡"}, text))
        self.hints = self.sequence.count("💡")
        assert self.hints <= 7
        seq_before_theme_word = tuple(itertools.takewhile(lambda ch: ch != "🟡", self.sequence))
        self.tries_before_theme_word = seq_before_theme_word.count("🔵")
        self.hints_before_theme_word = seq_before_theme_word.count("💡")

    def is_winning(self) -> bool:
        return True
