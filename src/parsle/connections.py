from dataclasses import dataclass, field
import re
from .game_result import GameResult


@dataclass
class Connections(GameResult):
    mistakes: int = field(metadata={"higher_is_better": False})

    def __init__(self, text: str):
        super().__init__("Connections", "https://www.nytimes.com/games/connections")
        match = re.match(r"Connections\nPuzzle #(\d+)", text, re.MULTILINE)
        assert match, "Not a Connections game"
        # Max. 3 mistakes + 4 right guesses
        assert sum(self.is_emoji_row(row) for row in text.splitlines()) <= 7
        self.age = int(match.group(1))
        self.mistakes = sum(self.is_mistake_row(row) for row in text.splitlines())

    @staticmethod
    def is_emoji_row(row: str) -> bool:
        """Checks if the row is made of four emojis with colored squares."""
        return len(row) == 4 and all(char in {"🟩", "🟨", "🟪", "🟦"} for char in row)

    @staticmethod
    def is_mistake_row(row: str) -> bool:
        return Connections.is_emoji_row(row) and any(ch1 != ch2 for ch1, ch2 in zip(row, row[1:]))

    def is_winning(self) -> bool:
        return self.mistakes < 4
