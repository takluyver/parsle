from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
import re
from typing import Any, Callable, Optional

# Regex functions take a string (capture group) and return any value
RegexFunction = Callable[[str], Any]


@dataclass
class GameResult(ABC):
    # The name of the game
    name: str
    # The URL where the game can be played. For documentation purposes
    url: str
    # How many days have passed since the game was first published
    age: Optional[int]

    @abstractmethod
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.age = None

    def __lt__(self, other):
        """
        Game results can be compared with the usual mathematical operators,
        providing a built-in way to compile rankings (i.e. `sorted(results)`).
        The ranking order is somewhat arbitrarily defined by the library author;
        users that prefer a different ranking logic can compare result members manually
        or override the comparison function.

        The general sorting function is:
          - only results from the same game can be compared.
          - a winning game is "greater than" a losing game
          - fields are compared in descending priority in the order they are declared,
           if they are annotated with "higher_is_better"
          - if a field is annotated with "higher_is_better": True, a game with a higher
           value of that field is greater than a game with a lower value; and vice versa
        This sorting can be overridden by subclasses.
        """
        if not isinstance(other, type(self)):
            raise ValueError()
        if self.is_winning() and not other.is_winning():
            return False
        if not self.is_winning() and other.is_winning():
            return True

        # Compare all fields in order
        for field in fields(self):
            higher_is_better = field.metadata.get("higher_is_better")
            # If the parameter is not defined, the fields are not to be compared, keep going
            if higher_is_better is None:
                continue
            # If two fields are the same, keep going
            self_value = self.__getattribute__(field.name)
            other_value = other.__getattribute__(field.name)
            if self_value == other_value:
                continue
            return (self_value < other_value) == higher_is_better
        return False

    def __le__(self, other):
        return (self == other) or (self < other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    @abstractmethod
    def is_winning(self) -> bool:
        raise NotImplementedError()


@dataclass
class RegexGameResult(GameResult):
    """
    RegexGameResult implements utilities for a game result that can be parsed
    with a regular expression. Capture groups are exported to self.raw, fields
    annotated with `from_group` will be set to that value, and fields that are
    also annotated with `transform` will have that function applied.

    For example:
        hardmode: bool = field(metadata={
            "higher_is_better": True,
            "from_group": "hardmode",
            "transform": lambda hardmode: bool(hardmode)
        })
    """

    # Raw capture groups from the regex
    raw: dict[str, str]

    def __init__(self, name: str, url: str, regex: str, text: str):
        super().__init__(name, url)
        pattern = re.compile(regex, flags=re.MULTILINE)
        match = pattern.search(text)
        assert match is not None

        self.raw = match.groupdict()
        for field in fields(self):
            group_name: Optional[str] = field.metadata.get("from_group")
            if group_name is None:
                continue
            value = self.raw[group_name]
            transform: Optional[RegexFunction] = field.metadata.get("transform")
            if transform is not None:
                value = transform(value)
            self.__setattr__(field.name, value)
