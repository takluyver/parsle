def parse_int(input: str) -> int:
    """
    Parses integers stripping thousands separators.
    """
    return int(input.replace(" ", "").replace(".", "").replace(",", ""))
