from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional

from parsle.utils import parse_int

from .game_result import RegexGameResult


@dataclass
class Wordle(RegexGameResult):
    hardmode: bool = field(
        metadata={
            "higher_is_better": True,
            "from_group": "hardmode",
            "transform": bool,
        }
    )
    tries: Optional[int] = field(
        metadata={
            "higher_is_better": False,
            "from_group": "score",
            "transform": lambda score: None if score == "X" else int(score),
        }
    )

    def __init__(self, text: str):
        super().__init__(
            "Wordle",
            "https://www.nytimes.com/games/wordle/index.html",
            # '🎉'.encode('unicode-escape') = \U0001f389
            regex=r"^Wordle (?P<age>[0-9.,]+)( \U0001f389)? (?P<score>\d+|X)/6(?P<hardmode>\*?)$",
            text=text,
        )
        self.age = parse_int(self.raw["age"])

    def is_winning(self) -> bool:
        return self.tries is not None
